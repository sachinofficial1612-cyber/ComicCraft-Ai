import React from 'react';
import { Panel } from '../types/comic';
import { SpeechBubbleOverlay } from './SpeechBubbleOverlay';
import { RefreshCw, MessageSquare, Edit3, Trash2, Image as ImageIcon } from 'lucide-react';

interface PanelCardProps {
  panel: Panel;
  onEdit: (panel: Panel) => void;
  onRegenerateImage: (panel: Panel) => void;
  onRegenerateStory: (panel: Panel) => void;
  onDelete?: (panel: Panel) => void;
  isRegenerating?: boolean;
}

export const PanelCard: React.FC<PanelCardProps> = ({
  panel,
  onEdit,
  onRegenerateImage,
  onRegenerateStory,
  onDelete,
  isRegenerating = false
}) => {
  return (
    <div className="group relative bg-slate-900 rounded-2xl border-4 border-slate-800 overflow-hidden shadow-2xl hover:border-sky-500/50 transition-all flex flex-col">
      {/* Top Header Badge */}
      <div className="bg-slate-950 px-4 py-2 flex items-center justify-between border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="comic-title text-sky-400 text-lg">PANEL #{panel.panel_number}</span>
          {panel.title && <span className="text-xs text-slate-400 truncate max-w-[150px]">— {panel.title}</span>}
        </div>
        <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full ${
          panel.status === 'completed' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
          panel.status === 'failed' ? 'bg-red-500/10 text-red-400 border border-red-500/20' :
          'bg-amber-500/10 text-amber-300 border border-amber-500/20 animate-pulse'
        }`}>
          {panel.status}
        </span>
      </div>

      {/* Image Artwork Canvas */}
      <div className="relative aspect-[4/3] bg-slate-950 flex items-center justify-center overflow-hidden">
        {panel.image_path ? (
          <img
            src={panel.image_path}
            alt={panel.scene_description || `Panel ${panel.panel_number}`}
            className={`w-full h-full object-cover transition-opacity duration-300 ${isRegenerating ? 'opacity-40 blur-sm' : 'opacity-100'}`}
          />
        ) : (
          <div className="flex flex-col items-center gap-2 text-slate-500 p-6 text-center">
            <ImageIcon className="w-10 h-10 animate-bounce" />
            <p className="text-xs">Artwork Pending Generation</p>
          </div>
        )}

        {/* Speech & Narration Overlay */}
        <SpeechBubbleOverlay
          narration={panel.narration}
          dialogue={panel.dialogue}
          soundEffect={panel.sound_effect}
        />

        {/* Loading Spinner during regeneration */}
        {isRegenerating && (
          <div className="absolute inset-0 bg-slate-950/60 backdrop-blur-xs flex flex-col items-center justify-center text-white">
            <RefreshCw className="w-8 h-8 animate-spin text-sky-400 mb-2" />
            <span className="text-xs font-semibold">Regenerating Panel...</span>
          </div>
        )}
      </div>

      {/* Panel Action Toolbar */}
      <div className="p-3 bg-slate-900 border-t border-slate-800 flex items-center justify-between gap-1 text-xs">
        <div className="flex items-center gap-1">
          <button
            onClick={() => onRegenerateImage(panel)}
            disabled={isRegenerating}
            className="flex items-center gap-1 px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-sky-300 rounded-lg font-medium transition-colors disabled:opacity-50"
            title="Regenerate Artwork Image Only"
          >
            <ImageIcon className="w-3.5 h-3.5" />
            <span>Image</span>
          </button>

          <button
            onClick={() => onRegenerateStory(panel)}
            disabled={isRegenerating}
            className="flex items-center gap-1 px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-amber-300 rounded-lg font-medium transition-colors disabled:opacity-50"
            title="Regenerate Dialogue & Narration"
          >
            <MessageSquare className="w-3.5 h-3.5" />
            <span>Story</span>
          </button>
        </div>

        <div className="flex items-center gap-1">
          <button
            onClick={() => onEdit(panel)}
            className="flex items-center gap-1 px-2.5 py-1.5 bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 rounded-lg font-medium border border-sky-500/20 transition-colors"
          >
            <Edit3 className="w-3.5 h-3.5" />
            <span>Edit</span>
          </button>

          {onDelete && (
            <button
              onClick={() => onDelete(panel)}
              className="p-1.5 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
              title="Delete Panel"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
