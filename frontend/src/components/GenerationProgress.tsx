import React from 'react';
import { CheckCircle2, Loader2, Circle, Sparkles } from 'lucide-react';
import { GenerationStatus } from '../types/comic';

interface GenerationProgressProps {
  status: GenerationStatus | null;
  error?: string | null;
}

export const GenerationProgress: React.FC<GenerationProgressProps> = ({ status, error }) => {
  const completedPanels = status?.completed_panels || 0;
  const totalPanels = status?.total_panels || 6;
  const progressPercent = status?.progress_percentage || 0;

  const stages = [
    { key: 'story', label: 'Understanding Story & Themes', done: true },
    { key: 'character', label: 'Building Character Bible', done: true },
    { key: 'outline', label: 'Planning Comic Panel Outline', done: true },
    { key: 'script', label: 'Writing Dialogue & Narration', done: true },
    {
      key: 'artwork',
      label: `Generating Artwork (${completedPanels} of ${totalPanels} panels completed)`,
      done: completedPanels >= totalPanels,
      active: completedPanels < totalPanels
    },
    { key: 'composition', label: 'Composing Final Comic Book', done: completedPanels >= totalPanels }
  ];

  return (
    <div className="max-w-xl mx-auto bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl text-center my-12">
      <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center mx-auto mb-6 shadow-xl shadow-sky-500/20">
        <Sparkles className="w-8 h-8 text-white animate-pulse" />
      </div>

      <h2 className="comic-title text-3xl text-white mb-2">Crafting Your AI Comic</h2>
      <p className="text-slate-400 text-sm mb-8">Generating story arc, character bible, artwork, and composition...</p>

      {/* Progress Bar */}
      <div className="w-full bg-slate-950 rounded-full h-3 mb-8 p-0.5 border border-slate-800 overflow-hidden">
        <div
          className="bg-gradient-to-r from-sky-500 to-indigo-500 h-full rounded-full transition-all duration-500"
          style={{ width: `${Math.max(10, progressPercent)}%` }}
        />
      </div>

      {/* Stage Items List */}
      <div className="space-y-3.5 text-left mb-6">
        {stages.map((stage, idx) => (
          <div key={idx} className="flex items-center gap-3 text-sm">
            {stage.done ? (
              <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
            ) : stage.active ? (
              <Loader2 className="w-5 h-5 text-sky-400 animate-spin shrink-0" />
            ) : (
              <Circle className="w-5 h-5 text-slate-700 shrink-0" />
            )}
            <span className={stage.done ? 'text-slate-200 font-medium' : stage.active ? 'text-sky-300 font-semibold' : 'text-slate-600'}>
              {stage.label}
            </span>
          </div>
        ))}
      </div>

      {error && (
        <div className="p-4 bg-red-950/50 border border-red-500/30 rounded-xl text-red-300 text-xs font-semibold">
          Generation Error: {error}
        </div>
      )}
    </div>
  );
};
