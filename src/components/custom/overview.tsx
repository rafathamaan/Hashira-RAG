import { motion } from 'framer-motion';
import { MessageCircle, BotIcon } from 'lucide-react';

export const Overview = () => {
  return (
    <>
    <motion.div
      key="overview"
      className="max-w-3xl mx-auto md:mt-20"
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.98 }}
      transition={{ delay: 0.75 }}
    >
      <div className="rounded-xl p-2 flex flex-col leading-relaxed text-center max-w-xl">
        
        <p>
          Welcome to <strong>Hashira.io</strong><br />
Instant answers from your docs, no manual searching.<br />
        </p>
      </div>
    </motion.div>
    </>
  );
};
