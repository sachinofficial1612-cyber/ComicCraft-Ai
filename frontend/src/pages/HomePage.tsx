import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Sparkles, ArrowRight, LayoutGrid, BookOpen, Layers, Wand2, ShieldCheck, Download } from 'lucide-react';
import { api } from '../services/api';

export const HomePage: React.FC = () => {
  const navigate = useNavigate();

  const handleTryDemo = async () => {
    try {
      const demo = await api.getDemoProject();
      navigate(`/comic/${demo.id}`);
    } catch (e) {
      console.error(e);
      navigate('/create');
    }
  };

  return (
    <div className="space-y-24 py-8">
      {/* Hero Section */}
      <section className="relative text-center max-w-4xl mx-auto space-y-6 pt-12">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sky-500/10 border border-sky-500/20 text-sky-400 text-xs font-semibold uppercase tracking-wider">
          <Sparkles className="w-4 h-4" /> Powered by Google Gemini & Image Models
        </div>

        <h1 className="comic-title text-5xl sm:text-7xl text-white tracking-wide leading-none">
          TURN YOUR STORY INTO A REAL <span className="text-sky-400 underline decoration-sky-500/50 decoration-wavy">COMIC</span>
        </h1>

        <p className="text-slate-300 text-lg sm:text-xl max-w-2xl mx-auto leading-relaxed">
          Write an idea. Let AI build the story, scenes, characters, artwork, and comic book.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <Link
            to="/create"
            className="flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-base rounded-2xl shadow-xl shadow-sky-500/25 transition-all transform hover:-translate-y-0.5"
          >
            <span>Create Your Comic</span>
            <ArrowRight className="w-5 h-5" />
          </Link>

          <button
            onClick={handleTryDemo}
            className="flex items-center gap-2 px-6 py-4 bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-800 font-semibold text-base rounded-2xl transition-colors"
          >
            <BookOpen className="w-5 h-5 text-amber-400" />
            <span>View Built-in Demo</span>
          </button>
        </div>

        {/* Hero Visual Mockup Preview */}
        <div className="pt-12 relative max-w-3xl mx-auto">
          <div className="bg-slate-900 border-4 border-slate-800 rounded-3xl p-6 shadow-2xl overflow-hidden group hover:border-sky-500/30 transition-all">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500" />
                <div className="w-3 h-3 rounded-full bg-amber-500" />
                <div className="w-3 h-3 rounded-full bg-emerald-500" />
              </div>
              <span className="text-xs font-mono text-slate-500">COMICCRAFT_PREVIEW_PAGE.PDF</span>
            </div>
            <div className="grid grid-cols-2 gap-4 aspect-[16/9] bg-slate-950 rounded-2xl p-4 border border-slate-800">
              <div className="relative rounded-xl overflow-hidden bg-slate-900 border border-slate-800 flex items-center justify-center">
                <span className="comic-title text-sky-400 text-2xl">PANEL #1</span>
                <div className="absolute bottom-2 left-2 bg-amber-200 text-black px-2 py-1 rounded text-[10px] font-bold border border-black">
                  "In the enchanted forest..."
                </div>
              </div>
              <div className="relative rounded-xl overflow-hidden bg-slate-900 border border-slate-800 flex items-center justify-center">
                <span className="comic-title text-indigo-400 text-2xl">PANEL #2</span>
                <div className="absolute top-2 right-2 speech-bubble px-2 py-1 text-[10px] font-bold">
                  "What is this glowing light?"
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Highlights Grid */}
      <section className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="p-6 bg-slate-900 border border-slate-800 rounded-3xl space-y-3">
          <div className="w-12 h-12 rounded-2xl bg-sky-500/10 text-sky-400 flex items-center justify-center">
            <Wand2 className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-white">Multi-Stage AI Pipeline</h3>
          <p className="text-slate-400 text-sm">
            Story understanding, character extraction, comic outline planning, and dialogue script generation.
          </p>
        </div>

        <div className="p-6 bg-slate-900 border border-slate-800 rounded-3xl space-y-3">
          <div className="w-12 h-12 rounded-2xl bg-amber-500/10 text-amber-400 flex items-center justify-center">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-white">Character & Style Consistency</h3>
          <p className="text-slate-400 text-sm">
            Maintains character bible visual specs and art style continuity across every panel.
          </p>
        </div>

        <div className="p-6 bg-slate-900 border border-slate-800 rounded-3xl space-y-3">
          <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center">
            <Download className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-white">Interactive Editor & Export</h3>
          <p className="text-slate-400 text-sm">
            Edit dialogue, speech bubbles, and regenerate individual panels. Export as PDF or PNG pages.
          </p>
        </div>
      </section>
    </div>
  );
};
