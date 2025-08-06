import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cx } from 'classix';
import { SparklesIcon } from './icons';
import { Markdown } from './markdown';
import { message } from "../../interfaces/interfaces"
import { MessageActions } from '@/components/custom/actions';

export const PreviewMessage = ({ message }: { message: message; }) => {
  const isAssistant = message.role === 'assistant';
  return (
    <motion.div
      className="w-full mx-auto max-w-3xl px-4 group/message"
      initial={{ y: 5, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      data-role={message.role}
    >
      <div
        className={cx(
          'flex gap-4 w-full px-3 py-2 rounded-xl',
          isAssistant
            ? 'backdrop-blur-md bg-white/70 dark:bg-zinc-500/60 shadow-lg border border-white/30 dark:border-zinc-500/40'
            : 'bg-zinc-700 text-white ml-auto max-w-2xl' // For user message bubble
        )}
      >
        {isAssistant && (
          <div className="size-8 flex items-center rounded-full justify-center ring-1 shrink-0 ring-border">
            <SparklesIcon size={14} />
          </div>
        )}
        <div className="flex flex-col w-full">
          {message.content && (
            <div className="flex flex-col gap-4 text-left">
              <Markdown>{message.content}</Markdown>
            </div>
          )}
          {isAssistant && <MessageActions message={message} />}
        </div>
      </div>
    </motion.div>
  );
};

export const ThinkingMessage = () => {
  const role = 'assistant';

  return (
    <motion.div
      className="w-full mx-auto max-w-3xl px-4 group/message "
      initial={{ y: 5, opacity: 0 }}
      animate={{ y: 0, opacity: 1, transition: { delay: 0.2 } }}
      data-role={role}
    >
      <div
        className={cx(
          'flex gap-4 group-data-[role=user]/message:px-3 w-full group-data-[role=user]/message:w-fit group-data-[role=user]/message:ml-auto group-data-[role=user]/message:max-w-2xl group-data-[role=user]/message:py-2 rounded-xl',
          'group-data-[role=user]/message:bg-muted'
        )}
      >
        <div className="size-8 flex items-center rounded-full justify-center ring-1 shrink-0 ring-border">
          <SparklesIcon size={14} />
          </div>
      <div className=" ">
      <span className="animate-bounce inline-block w-2 h-2 bg-blue-600 rounded-full"></span>
      <span className="animate-bounce delay-150 inline-block w-2 h-2 bg-blue-600 rounded-full"></span>
      <span className="animate-bounce delay-300 inline-block w-2 h-2 bg-blue-600 rounded-full"></span>
    </div>
        </div>
      

    </motion.div>
  );
};
