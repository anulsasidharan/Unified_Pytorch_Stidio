import { useCallback, useEffect, useRef, useState } from 'react';
import { Bot, Loader2, MessageSquare, Send, Sparkles } from 'lucide-react';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { apiClient } from '@/lib/api-client';
import type { ChatMessageDto } from '@dsa-studio/shared';

interface ChatPanelProps {
  questionId?: string;
  code?: string;
  language?: string;
  compact?: boolean;
}

export function ChatPanel({ questionId, code, language, compact = false }: ChatPanelProps) {
  const [messages, setMessages] = useState<ChatMessageDto[]>([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState<string | undefined>();
  const [loading, setLoading] = useState(false);
  const [hintTier, setHintTier] = useState(0);
  const scrollRef = useRef<HTMLDivElement>(null);

  const appendAssistant = useCallback((content: string, messageType = 'query') => {
    setMessages((prev) => [
      ...prev,
      {
        id: crypto.randomUUID(),
        role: 'assistant',
        content,
        messageType,
        createdAt: new Date().toISOString(),
      },
    ]);
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages, loading]);

  async function sendMessage(text: string) {
    if (!text.trim() || loading) return;

    setMessages((prev) => [
      ...prev,
      {
        id: crypto.randomUUID(),
        role: 'user',
        content: text,
        messageType: 'query',
        createdAt: new Date().toISOString(),
      },
    ]);
    setInput('');
    setLoading(true);

    try {
      const result = await apiClient.chatQuery({
        message: text,
        questionId,
        sessionId,
      });
      setSessionId(result.sessionId);
      appendAssistant(result.reply);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Chat failed');
    } finally {
      setLoading(false);
    }
  }

  async function handleAiHint(showApproach = false) {
    if (!questionId || loading) return;
    setLoading(true);
    try {
      const result = await apiClient.chatHint({ questionId, showApproach, sessionId });
      setSessionId(result.sessionId);
      setHintTier(result.tier);
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'user',
          content: showApproach ? 'Show approach' : `AI hint (tier ${result.tier})`,
          messageType: 'hint',
          createdAt: new Date().toISOString(),
        },
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: result.hint,
          messageType: 'hint',
          createdAt: new Date().toISOString(),
        },
      ]);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Hint failed');
    } finally {
      setLoading(false);
    }
  }

  async function handleCodeReview() {
    if (!questionId || !code?.trim() || loading) {
      toast.error('Write some code before requesting a review');
      return;
    }
    setLoading(true);
    try {
      const result = await apiClient.chatReview({
        questionId,
        code,
        language: language ?? 'python',
        sessionId,
      });
      setSessionId(result.sessionId);
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'user',
          content: 'Review my code',
          messageType: 'review',
          createdAt: new Date().toISOString(),
        },
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: result.review,
          messageType: 'review',
          createdAt: new Date().toISOString(),
        },
      ]);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Review failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card className={compact ? '' : 'h-full'}>
      <CardHeader className="py-3">
        <CardTitle className="flex items-center gap-2 text-sm font-medium">
          <Bot className="h-4 w-4 text-primary" />
          AI Assistant
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3 pb-4">
        {questionId && (
          <div className="flex flex-wrap gap-2">
            <Button size="sm" variant="outline" onClick={() => handleAiHint(false)} disabled={loading}>
              <Sparkles className="mr-1 h-3 w-3" />
              AI Hint {hintTier > 0 ? `(${hintTier}/3)` : ''}
            </Button>
            {hintTier >= 2 && (
              <Button size="sm" variant="outline" onClick={() => handleAiHint(true)} disabled={loading}>
                Show approach
              </Button>
            )}
            {code && (
              <Button size="sm" variant="outline" onClick={handleCodeReview} disabled={loading}>
                Review code
              </Button>
            )}
          </div>
        )}

        <div
          ref={scrollRef}
          className={`space-y-3 overflow-y-auto rounded-md border bg-muted/30 p-3 ${compact ? 'max-h-48' : 'max-h-72'}`}
        >
          {messages.length === 0 && (
            <p className="text-center text-xs text-muted-foreground">
              Ask about DSA concepts, request hints, or get code feedback.
            </p>
          )}
          {messages.map((m) => (
            <div
              key={m.id}
              className={`rounded-md px-3 py-2 text-sm ${
                m.role === 'user'
                  ? 'ml-6 bg-primary text-primary-foreground'
                  : 'mr-6 bg-background border'
              }`}
            >
              <p className="whitespace-pre-wrap">{m.content}</p>
            </div>
          ))}
          {loading && (
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <Loader2 className="h-3 w-3 animate-spin" />
              Thinking…
            </div>
          )}
        </div>

        <form
          className="flex gap-2"
          onSubmit={(e) => {
            e.preventDefault();
            sendMessage(input);
          }}
        >
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a DSA question…"
            disabled={loading}
            aria-label="Chat message"
          />
          <Button type="submit" size="icon" disabled={loading || !input.trim()} aria-label="Send">
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

interface ChatHistorySidebarProps {
  onSelectSession: (sessionId: string) => void;
  activeSessionId?: string;
}

export function ChatHistorySidebar({ onSelectSession, activeSessionId }: ChatHistorySidebarProps) {
  const [items, setItems] = useState<
    Array<{ sessionId: string; title: string; updatedAt: string }>
  >([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient
      .getChatHistory()
      .then((data) =>
        setItems(
          data.items.map((i) => ({
            sessionId: i.sessionId,
            title: i.title,
            updatedAt: i.updatedAt,
          })),
        ),
      )
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, [activeSessionId]);

  if (loading) return <p className="text-sm text-muted-foreground">Loading history…</p>;
  if (items.length === 0) return <p className="text-sm text-muted-foreground">No chat history yet.</p>;

  return (
    <ul className="space-y-1">
      {items.map((item) => (
        <li key={item.sessionId}>
          <button
            type="button"
            onClick={() => onSelectSession(item.sessionId)}
            className={`flex w-full items-start gap-2 rounded-md px-3 py-2 text-left text-sm transition-colors hover:bg-accent ${
              activeSessionId === item.sessionId ? 'bg-accent' : ''
            }`}
          >
            <MessageSquare className="mt-0.5 h-4 w-4 shrink-0 text-muted-foreground" />
            <span>
              <span className="line-clamp-1 font-medium">{item.title}</span>
              <span className="block text-xs text-muted-foreground">
                {new Date(item.updatedAt).toLocaleDateString()}
              </span>
            </span>
          </button>
        </li>
      ))}
    </ul>
  );
}
