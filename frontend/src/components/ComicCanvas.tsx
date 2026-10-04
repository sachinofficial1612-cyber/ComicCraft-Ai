import React from 'react';
import { Project, Panel } from '../types/comic';
import { PanelCard } from './PanelCard';
import { Plus } from 'lucide-react';

interface ComicCanvasProps {
  project: Project;
  onEditPanel: (panel: Panel) => void;
  onRegenerateImage: (panel: Panel) => void;
  onRegenerateStory: (panel: Panel) => void;
  onDeletePanel: (panel: Panel) => void;
  onAddPanel: () => void;
  regeneratingPanelId?: string | null;
}

export const ComicCanvas: React.FC<ComicCanvasProps> = ({
  project,
  onEditPanel,
  onRegenerateImage,
  onRegenerateStory,
  onDeletePanel,
  onAddPanel,
  regeneratingPanelId
}) => {
  const panels = project.panels || [];
  const gridColsClass =
    panels.length <= 4 ? 'grid-cols-1 md:grid-cols-2' :
    panels.length <= 6 ? 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3' :
    'grid-cols-1 sm:grid-cols-2 lg:grid-cols-4';

  return (
    <div className="space-y-8">
      {/* Comic Header Box */}
      <div className="bg-slate-900 border-4 border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <span className="text-xs uppercase font-extrabold tracking-widest text-sky-400 block mb-1">
            COMICCRAFT ORIGINAL • {project.art_style} STYLE
          </span>
          <h1 className="comic-title text-3xl sm:text-5xl text-white tracking-wide">{project.title}</h1>
          <p className="text-slate-400 text-sm mt-2 max-w-2xl leading-relaxed">{project.original_prompt}</p>
        </div>

        <div className="flex flex-wrap items-center gap-3 bg-slate-950 px-4 py-3 rounded-2xl border border-slate-800 text-xs font-semibold text-slate-300 shrink-0">
          <div><span className="text-slate-500 block">CHARACTER</span>{project.character_name}</div>
          <div className="w-px h-6 bg-slate-800" />
          <div><span className="text-slate-500 block">SETTING</span>{project.setting}</div>
          <div className="w-px h-6 bg-slate-800" />
          <div><span className="text-slate-500 block">PANELS</span>{panels.length}</div>
        </div>
      </div>

      {/* Panels Grid */}
      <div className={`grid ${gridColsClass} gap-6`}>
        {panels.map((panel) => (
          <PanelCard
            key={panel.id}
            panel={panel}
            onEdit={onEditPanel}
            onRegenerateImage={onRegenerateImage}
            onRegenerateStory={onRegenerateStory}
            onDelete={onDeletePanel}
            isRegenerating={regeneratingPanelId === panel.id}
          />
        ))}

        {/* Add Panel Card Button */}
        <button
          onClick={onAddPanel}
          className="group min-h-[320px] rounded-2xl border-4 border-dashed border-slate-800 hover:border-sky-500/50 bg-slate-900/40 hover:bg-slate-900/80 flex flex-col items-center justify-center p-6 text-slate-500 hover:text-sky-400 transition-all cursor-pointer"
        >
          <div className="w-12 h-12 rounded-full bg-slate-800 group-hover:bg-sky-500/20 flex items-center justify-center mb-3 transition-colors">
            <Plus className="w-6 h-6" />
          </div>
          <span className="font-semibold text-sm">Add New Panel</span>
          <span className="text-xs text-slate-600 mt-1">Append next panel scene</span>
        </button>
      </div>
    </div>
  );
};
