import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Sparkles, BookOpen, PlusCircle, LayoutGrid, Cpu } from 'lucide-react';
import { api } from '../services/api';

export const Navbar: React.FC = () => {
  const location = useLocation();
  const [aiConfigured, setAiConfigured] = useState<boolean | null>(null);

  useEffect(() => {
    api.getAIHealth()
      .then(data => setAiConfigured(data.configured))
      .catch(() => setAiConfigured(false));
  }, []);

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="sticky top-0 z-40 bg-slate-900/90 backdrop-blur-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20 group-hover:scale-105 transition-transform">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <span className="comic-title text-2xl text-white tracking-wide">COMICCRAFT</span>
            <span className="text-[10px] block text-sky-400 font-semibold tracking-wider -mt-1 uppercase">AI Story Creator</span>
          </div>
        </Link>

        {/* Navigation links */}
        <nav className="flex items-center gap-2">
          <Link
            to="/create"
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              isActive('/create')
                ? 'bg-sky-500 text-white shadow-md shadow-sky-500/20'
                : 'text-slate-300 hover:bg-slate-800 hover:text-white'
            }`}
          >
            <PlusCircle className="w-4 h-4" />
            <span>Create Comic</span>
          </Link>

          <Link
            to="/dashboard"
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              isActive('/dashboard')
                ? 'bg-sky-500 text-white shadow-md shadow-sky-500/20'
                : 'text-slate-300 hover:bg-slate-800 hover:text-white'
            }`}
          >
            <LayoutGrid className="w-4 h-4" />
            <span>Comic Shelf</span>
          </Link>

          {/* AI Config status pill */}
          <div
            className={`ml-2 px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1.5 border ${
              aiConfigured === true
                ? 'bg-emerald-950/60 border-emerald-500/30 text-emerald-400'
                : 'bg-amber-950/60 border-amber-500/30 text-amber-300'
            }`}
            title={aiConfigured ? 'Gemini API Connected' : 'Gemini Key Not Set — Utilizing Smart Canvas Engine'}
          >
            <Cpu className="w-3.5 h-3.5" />
            <span>{aiConfigured === true ? 'Gemini AI Active' : 'Fallback Engine Active'}</span>
          </div>
        </nav>
      </div>
    </header>
  );
};
