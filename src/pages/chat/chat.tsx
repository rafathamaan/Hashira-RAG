import { ChatInput } from "@/components/custom/chatinput";
import { PreviewMessage, ThinkingMessage } from "../../components/custom/message";
import { useScrollToBottom } from '@/components/custom/use-scroll-to-bottom';
import { useState, useRef } from "react";
import { message } from "../../interfaces/interfaces"
import { Overview } from "@/components/custom/overview";
import { Header } from "@/components/custom/header";
import { v4 as uuidv4 } from 'uuid';

export function Chat() {
  const [messagesContainerRef, messagesEndRef] = useScrollToBottom<HTMLDivElement>();
  const [messages, setMessages] = useState<message[]>([]);
  const [question, setQuestion] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const abortControllerRef = useRef<AbortController | null>(null);

  async function handleSubmit(text?: string) {
    if (isLoading) return;

    const messageText = text || question;
    if (!messageText.trim()) return;

    const traceId = uuidv4();
    setMessages(prev => [...prev, { content: messageText, role: "user", id: traceId }]);
    setQuestion("");
    setIsLoading(true);

    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: messageText }),
        signal: abortControllerRef.current.signal
      });

      if (!response.ok) throw new Error("Failed to get response from server");

      const data = await response.json();
      const answer = data.answer || "No response received.";

      setMessages(prev => [...prev, { content: answer, role: "assistant", id: uuidv4() }]);
    } catch (error) {
      console.error("API error:", error);
      setMessages(prev => [...prev, { content: "⚠️ Error connecting to the server.", role: "assistant", id: uuidv4() }]);
    } finally {
      setIsLoading(false);
    }
  }

  const isBlurActive = !!question || isLoading;

  return (
    <div 
      className="flex flex-col min-w-0 h-dvh bg-background relative"
      style={{
        backgroundImage: "url('src/assets/fonts/images/hashira-logomark.svg')",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        backgroundSize: "25vh",
        opacity: 1
      }}
    >
      <Header />
      <div 
        ref={messagesContainerRef}
        className={`
          flex flex-col min-w-0 gap-6 flex-1 overflow-y-scroll pt-4
          transition-all duration-200
          ${isBlurActive ? "backdrop-blur-md bg-white/30 dark:bg-black/20" : ""}
        `}
      >
        {messages.length === 0 && <Overview />}
        {messages.map((message, index) => (
          <PreviewMessage key={index} message={message} />
        ))}
        {isLoading && <ThinkingMessage />}
        <div ref={messagesEndRef} className="shrink-0 min-w-[24px] min-h-[24px]" />
      </div>
      {/* Floating, glassy input area */}
      <div className="flex mx-auto px-4 pb-4 md:pb-6 gap-2 w-full md:max-w-3xl">
        <div className={`
          w-full rounded-2xl transition-all duration-200
          backdrop-blur-lg bg-white/70 dark:bg-zinc-900/60
          shadow-2xl border border-white/40 dark:border-zinc-600/40
          py-2 px-4
          ${isBlurActive ? "ring-2 ring-blue-400/30" : ""}
        `}>
          <ChatInput  
            question={question}
            setQuestion={setQuestion}
            onSubmit={handleSubmit}
            isLoading={isLoading}
          />
        </div>
      </div>
    </div>
  );
}
