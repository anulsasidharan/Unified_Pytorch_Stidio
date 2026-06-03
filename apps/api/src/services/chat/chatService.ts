import type { ChatMessageType } from '@prisma/client';
import { completeLLM } from '../../lib/llm/index.js';
import { prisma } from '../../lib/prisma.js';
import { AppError } from '../../middleware/errorHandler.js';
import {
  DSA_SYSTEM_PROMPT,
  buildQuestionContext,
  formatQuestionContextBlock,
  getUserProfileContext,
} from './contextBuilder.js';

async function getOrCreateSession(
  userId: string,
  questionId?: string,
  sessionId?: string,
): Promise<{ sessionId: string }> {
  if (sessionId) {
    const existing = await prisma.chatSession.findFirst({
      where: { sessionId, userId },
    });
    if (!existing) {
      throw new AppError(404, 'NOT_FOUND', 'Chat session not found');
    }
    return { sessionId: existing.sessionId };
  }

  const session = await prisma.chatSession.create({
    data: {
      userId,
      questionId: questionId ?? null,
      title: questionId ? 'Practice session' : 'General chat',
    },
  });

  return { sessionId: session.sessionId };
}

async function persistExchange(
  sessionId: string,
  userContent: string,
  assistantContent: string,
  messageType: ChatMessageType,
  tokensUsed: number,
): Promise<void> {
  await prisma.$transaction([
    prisma.chatMessage.create({
      data: {
        sessionId,
        role: 'user',
        content: userContent,
        messageType,
      },
    }),
    prisma.chatMessage.create({
      data: {
        sessionId,
        role: 'assistant',
        content: assistantContent,
        messageType,
        tokensUsed,
      },
    }),
    prisma.chatSession.update({
      where: { sessionId },
      data: { updatedAt: new Date() },
    }),
  ]);
}

export async function chatQuery(
  userId: string,
  message: string,
  questionId?: string,
  sessionId?: string,
) {
  const { sessionId: sid } = await getOrCreateSession(userId, questionId, sessionId);

  const contextParts = [await getUserProfileContext(userId)];

  if (questionId) {
    const qCtx = await buildQuestionContext(userId, questionId);
    contextParts.push(formatQuestionContextBlock(qCtx));
  }

  const result = await completeLLM({
    messages: [
      { role: 'system', content: DSA_SYSTEM_PROMPT },
      {
        role: 'system',
        content: `Context:\n${contextParts.filter(Boolean).join('\n\n')}`,
      },
      { role: 'user', content: message },
    ],
    maxTokens: 1024,
  });

  await persistExchange(sid, message, result.content, 'query', result.tokensUsed);

  return {
    sessionId: sid,
    reply: result.content,
    tokensUsed: result.tokensUsed,
    provider: result.provider,
  };
}

export async function chatHint(
  userId: string,
  questionId: string,
  showApproach = false,
  sessionId?: string,
) {
  const qCtx = await buildQuestionContext(userId, questionId);
  const { sessionId: sid } = await getOrCreateSession(userId, questionId, sessionId);

  const existingTier = await prisma.userHintTier.findUnique({
    where: { userId_questionId: { userId, questionId } },
  });

  const nextTier = showApproach ? Math.max(existingTier?.hintTier ?? 0, 3) : (existingTier?.hintTier ?? 0) + 1;

  const tierInstruction = showApproach
    ? 'The user explicitly requested to see the approach. Provide the approach name and state definition, but still avoid giving complete copy-paste code unless they insist.'
    : `Provide hint tier ${nextTier} only. Tier 1: smallest subproblem. Tier 2: build from smaller. Tier 3: approach name + state. Never exceed one tier per response.`;

  const userMessage = showApproach
    ? 'Please show me the approach for this problem.'
    : `I'm stuck on this problem. Give me hint tier ${nextTier}.`;

  const result = await completeLLM({
    messages: [
      { role: 'system', content: DSA_SYSTEM_PROMPT },
      {
        role: 'system',
        content: `${formatQuestionContextBlock(qCtx)}\n\n${tierInstruction}`,
      },
      { role: 'user', content: userMessage },
    ],
    maxTokens: 512,
    temperature: 0.3,
  });

  await prisma.userHintTier.upsert({
    where: { userId_questionId: { userId, questionId } },
    create: { userId, questionId, hintTier: nextTier },
    update: { hintTier: nextTier },
  });

  await persistExchange(sid, userMessage, result.content, 'hint', result.tokensUsed);

  return {
    sessionId: sid,
    hint: result.content,
    tier: nextTier,
    totalTiers: 3,
    showApproach,
    tokensUsed: result.tokensUsed,
    provider: result.provider,
  };
}

export async function chatReview(
  userId: string,
  questionId: string,
  code: string,
  language: string,
  sessionId?: string,
) {
  if (!code.trim()) {
    throw new AppError(400, 'VALIDATION_ERROR', 'Code is required for review');
  }

  const qCtx = await buildQuestionContext(userId, questionId);
  const { sessionId: sid } = await getOrCreateSession(userId, questionId, sessionId);

  const userMessage = `Review my ${language} solution:\n\`\`\`${language}\n${code}\n\`\`\``;

  const result = await completeLLM({
    messages: [
      { role: 'system', content: DSA_SYSTEM_PROMPT },
      {
        role: 'system',
        content: `${formatQuestionContextBlock(qCtx)}\n\nAnalyze the submitted code for correctness, time complexity, space complexity, and optimization suggestions. Use the format: ✅ Correct logic, ⚠️ Time complexity, 💡 Suggestion.`,
      },
      { role: 'user', content: userMessage },
    ],
    maxTokens: 1024,
    temperature: 0.2,
  });

  await persistExchange(sid, userMessage, result.content, 'review', result.tokensUsed);

  return {
    sessionId: sid,
    review: result.content,
    tokensUsed: result.tokensUsed,
    provider: result.provider,
  };
}

export async function getChatHistory(userId: string, page: number, limit: number) {
  const skip = (page - 1) * limit;

  const [sessions, total] = await Promise.all([
    prisma.chatSession.findMany({
      where: { userId },
      orderBy: { updatedAt: 'desc' },
      skip,
      take: limit,
      include: {
        question: {
          select: { title: true, slug: true },
        },
        messages: {
          orderBy: { createdAt: 'desc' },
          take: 2,
        },
      },
    }),
    prisma.chatSession.count({ where: { userId } }),
  ]);

  const items = sessions.map((s) => {
    const lastMessage = s.messages[0];
    return {
      sessionId: s.sessionId,
      title: s.title ?? s.question?.title ?? 'Chat',
      questionId: s.questionId,
      questionSlug: s.question?.slug ?? null,
      lastMessage: lastMessage
        ? {
            role: lastMessage.role,
            content: lastMessage.content.slice(0, 200),
            messageType: lastMessage.messageType,
            createdAt: lastMessage.createdAt.toISOString(),
          }
        : null,
      updatedAt: s.updatedAt.toISOString(),
      createdAt: s.createdAt.toISOString(),
    };
  });

  return { items, total };
}

export async function getSessionMessages(userId: string, sessionId: string) {
  const session = await prisma.chatSession.findFirst({
    where: { sessionId, userId },
    include: {
      messages: { orderBy: { createdAt: 'asc' } },
      question: { select: { title: true, slug: true, questionId: true } },
    },
  });

  if (!session) {
    throw new AppError(404, 'NOT_FOUND', 'Chat session not found');
  }

  return {
    sessionId: session.sessionId,
    questionId: session.questionId,
    question: session.question,
    messages: session.messages.map((m) => ({
      id: m.messageId,
      role: m.role,
      content: m.content,
      messageType: m.messageType,
      createdAt: m.createdAt.toISOString(),
    })),
  };
}
