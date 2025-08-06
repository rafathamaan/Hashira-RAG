export function ThinkingMessage() {
  return (
    <div className="flex items-center gap-2 py-2 px-4 text-sm text-muted-foreground">
      <span>Assistant is typing</span>
      <div className="flex space-x-1">
        <span className="animate-bounce inline-block w-2 h-2 bg-blue-600 rounded-full"></span>
        <span className="animate-bounce delay-150 inline-block w-2 h-2 bg-blue-600 rounded-full"></span>
        <span className="animate-bounce delay-300 inline-block w-2 h-2 bg-blue-600 rounded-full"></span>
      </div>
    </div>
  );
}
