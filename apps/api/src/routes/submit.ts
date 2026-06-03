import { Router } from 'express';
import { prisma } from '../lib/prisma.js';
import { success } from '../lib/response.js';
import { AppError } from '../middleware/errorHandler.js';
import { requireAuth, type AuthenticatedRequest } from '../middleware/auth.js';
import { validate } from '../middleware/validate.js';
import { gradeSubmission } from '../services/grading.js';
import { recordAttempt } from '../services/progress.js';
import { runSchema, submitSchema } from '../validators/submit.js';

export const submitRouter = Router();

submitRouter.post('/submit', requireAuth, validate(submitSchema), async (req: AuthenticatedRequest, res, next) => {
  try {
    const { questionId, language, code } = req.body;

    const question = await prisma.question.findFirst({
      where: { questionId, isActive: true },
      include: { testCases: { orderBy: { orderIndex: 'asc' } } },
    });

    if (!question) {
      throw new AppError(404, 'NOT_FOUND', 'Question not found');
    }

    const grading = await gradeSubmission(language, code, question.testCases);

    await recordAttempt(
      req.userId!,
      question.questionId,
      question.topicId,
      language,
      code,
      grading.status,
      grading.testCasesPassed,
      grading.totalTestCases,
      grading.executionTimeMs,
      grading.memoryUsedMb,
    );

    res.json(
      success({
        status: grading.status,
        testCasesPassed: grading.testCasesPassed,
        totalTestCases: grading.totalTestCases,
        executionTimeMs: grading.executionTimeMs,
        memoryUsedMb: grading.memoryUsedMb,
        results: grading.results.map((r) => ({
          testCaseId: r.testCaseId,
          passed: r.passed,
          isSample: r.isSample,
          executionTimeMs: r.executionTimeMs,
          ...(r.isSample
            ? {
                expectedOutput: r.expectedOutput,
                actualOutput: r.actualOutput,
                error: r.error,
              }
            : { error: r.error }),
        })),
      }),
    );
  } catch (error) {
    next(error);
  }
});

submitRouter.post('/run', requireAuth, validate(runSchema), async (req: AuthenticatedRequest, res, next) => {
  try {
    const { questionId, language, code } = req.body;

    const question = await prisma.question.findFirst({
      where: { questionId, isActive: true },
      include: {
        testCases: {
          where: { isSample: true },
          orderBy: { orderIndex: 'asc' },
        },
      },
    });

    if (!question) {
      throw new AppError(404, 'NOT_FOUND', 'Question not found');
    }

    const grading = await gradeSubmission(language, code, question.testCases, {
      sampleOnly: true,
    });

    res.json(
      success({
        status: grading.status,
        testCasesPassed: grading.testCasesPassed,
        totalTestCases: grading.totalTestCases,
        executionTimeMs: grading.executionTimeMs,
        results: grading.results,
      }),
    );
  } catch (error) {
    next(error);
  }
});
