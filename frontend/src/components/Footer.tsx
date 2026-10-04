import React from 'react';
import { Sparkles } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-950 border-t border-slate-900 py-8 text-center text-sm text-slate-500">
      <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-sky-400" />
          <span className="font-semibold text-slate-300">ComicCraft AI</span>
          <span>— Full-Stack AI Comic Generator</span>
        </div>
        <div className="text-xs">
          Built with React, TypeScript, FastAPI, SQLAlchemy & Google Gemini API.
        </div>
      </div>
    </footer>
  );
};
