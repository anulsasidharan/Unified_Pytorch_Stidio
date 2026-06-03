import { useCallback, useEffect, useRef, useState } from 'react';
import { Bot, Loader2, Plus, Send } from 'lucide-react';
import { toast, Toaster } from 'sonner';
import { AuthDialog } from '@/components/auth/AuthDialog';
import { ChatHistorySidebar } from '@/components/chat/ChatPanel';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import { apiClient } from '@/lib/api-client';
import { useAuthStore } from '@/store/authStore';
import type { ChatMessageDto } from '@dsa-studio/shared';

export function AssistantPage() {
  const token = useAuthStore((s) => s.token);
  const [authOpen, setAuthOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessageDto[]>([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState<string | undefined>();
  const [loading, setLoading] = useState(false);
  const [loadingSession, setLoadingSession] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages, loading]);

  const loadSession = useCallback(async (sid: string) => {
    setLoadingSession(true);
    try {
      const data = await apiClient.getChatSession(sid);
      setSessionId(data.sessionId);
      setMessages(data.messages);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load session');
    } finally {
      setLoadingSession(false);
    }
  }, []);

  function startNewChat() {
    setSessionId(undefined);
    setMessages([]);
    setInput('');
  }

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
      const result = await apiClient.chatQuery({ message: text, sessionId });
      setSessionId(result.sessionId);
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: result.reply,
          messageType: 'query',
          createdAt: new Date().toISOString(),
        },
      ]);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Chat failed');
    } finally {
      setLoading(false);
    }
  }

  if (!token) {
    return (
      <div className="space-y-6">
        <Toaster richColors position="top-center" />
        <AuthDialog open={authOpen} onOpenChange={setAuthOpen} />
        <h1 className="text-3xl font-bold tracking-tight">AI Assistant</h1>
        <Card>
          <CardContent className="flex flex-col items-center gap-4 py-12">
            <Bot className="h-12 w-12 text-muted-foreground" />
            <p className="text-muted-foreground">Sign in to chat with the DSA assistant.</p>
            <Button onClick={() => setAuthOpen(true)}>Sign in</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Toaster richColors position="top-center" />
      <section className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">AI Assistant</h1>
        <p className="max-w-2xl text-muted-foreground">
          Get concept explanations, progressive hints, and code review — focused on data structures
          and algorithms.
        </p>
      </section>

      <div className="grid gap-6 lg:grid-cols-[240px_1fr]">
        <Card>
          <CardHeader className="py-4">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm">History</CardTitle>
              <Button size="sm" variant="ghost" onClick={startNewChat} aria-label="New chat">
                <Plus className="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>
          <CardContent className="pb-4">
            <ChatHistorySidebar onSelectSession={loadSession} activeSessionId={sessionId} />
          </CardContent>
        </Card>

        <Card className="flex min-h-[480px] flex-col">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bot className="h-5 w-5 text-primary" />
              Chat
            </CardTitle>
            <CardDescription>
              Ask about algorithms, complexity, interview prep, or practice strategies.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-1 flex-col gap-4">
            {loadingSession ? (
              <Skeleton className="flex-1" />
            ) : (
              <div
                ref={scrollRef}
                className="flex-1 space-y-3 overflow-y-auto rounded-md border bg-muted/20 p-4"
              >
                {messages.length === 0 && (
                  <div className="flex h-full flex-col items-center justify-center gap-2 text-center text-muted-foreground">
                    <Bot className="h-10 w-10 opacity-50" />
                    <p className="text-sm">
                      Try: &quot;Explain dynamic programming&quot; or &quot;How do I approach graph
                      problems?&quot;
                    </p>
                  </div>
                )}
                {messages.map((m) => (
                  <div
                    key={m.id}
                    className={`max-w-[85%] rounded-lg px-4 py-2 text-sm ${
                      m.role === 'user'
                        ? 'ml-auto bg-primary text-primary-foreground'
                        : 'mr-auto border bg-background'
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{m.content}</p>
                    <p className="mt-1 text-[10px] opacity-60">
                      {new Date(m.createdAt).toLocaleTimeString()}
                    </p>
                  </div>
                ))}
                {loading && (
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Assistant is thinking…
                  </div>
                )}
              </div>
            )}

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
                placeholder="Ask your DSA question…"
                disabled={loading || loadingSession}
                className="flex-1"
              />
              <Button type="submit" disabled={loading || !input.trim()}>
                <Send className="mr-1 h-4 w-4" />
                Send
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
