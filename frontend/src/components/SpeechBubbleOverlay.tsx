import React from 'react';
import { DialogueItem } from '../types/comic';

interface SpeechBubbleOverlayProps {
  dialogue?: DialogueItem[];
  narration?: string;
  soundEffect?: string;
}

export const SpeechBubbleOverlay: React.FC<SpeechBubbleOverlayProps> = ({ dialogue, narration, soundEffect }) => {
  return (
    <div className="absolute inset-0 pointer-events-none p-4 flex flex-col justify-between overflow-hidden">
      {/* Top Narration Box */}
      {narration && (
        <div className="self-start max-w-[90%] bg-amber-200 text-slate-950 px-3.5 py-2 rounded border-2 border-black font-semibold text-xs leading-snug shadow-md transform -rotate-1">
          <span className="font-extrabold uppercase text-[10px] block text-amber-900 tracking-wider">NARRATION</span>
          {narration}
        </div>
      )}

      {/* Middle Sound Effect */}
      {soundEffect && (
        <div className="self-center comic-title text-4xl text-yellow-300 drop-shadow-[0_4px_4px_rgba(0,0,0,0.9)] transform rotate-6 tracking-widest animate-pulse">
          {soundEffect}
        </div>
      )}

      {/* Bottom Speech Bubbles */}
      <div className="flex flex-col gap-2 max-w-[85%] self-end">
        {dialogue && dialogue.map((item, idx) => {
          const type = item.bubble_type || 'speech';

          if (type === 'thought') {
            return (
              <div key={idx} className="bg-white border-2 border-black rounded-full px-4 py-2 text-black text-xs font-semibold shadow-lg">
                <span className="text-[10px] text-slate-500 font-bold block">{item.speaker} (thinks):</span>
                "{item.text}"
              </div>
            );
          }

          if (type === 'shout') {
            return (
              <div key={idx} className="bg-red-100 border-3 border-red-600 text-red-950 px-4 py-2 rounded-xl font-bold text-xs uppercase tracking-wide shadow-xl transform rotate-1">
                <span className="text-[10px] text-red-700 block">{item.speaker}:</span>
                "{item.text}"
              </div>
            );
          }

          // Default Speech Bubble
          return (
            <div key={idx} className="speech-bubble px-3.5 py-2 text-xs leading-snug shadow-xl">
              <span className="font-bold text-sky-900 text-[10px] block">{item.speaker}</span>
              "{item.text}"
            </div>
          );
        })}
      </div>
    </div>
  );
};
