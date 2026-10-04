import React, { useState } from 'react';
import { Panel, DialogueItem } from '../types/comic';
import { X, Plus, Trash2, Save, RefreshCw, Sparkles, MessageSquare, Image as ImageIcon } from 'lucide-react';

interface PanelEditorProps {
  panel: Panel;
  onSave: (panelId: string, updates: Partial<Panel>) => Promise<void>;
  onClose: () => void;
  onRegenerateImage: (panel: Panel) => Promise<void>;
  onRegenerateStory: (panel: Panel) => Promise<void>;
}

export const PanelEditor: React.FC<PanelEditorProps> = ({
  panel,
  onSave,
  onClose,
  onRegenerateImage,
  onRegenerateStory,
}) => {
  const [title, setTitle] = useState(panel.title || '');
  const [narration, setNarration] = useState(panel.narration || '');
  const [soundEffect, setSoundEffect] = useState(panel.sound_effect || '');
  const [imagePrompt, setImagePrompt] = useState(panel.image_prompt || '');
  const [sceneDescription, setSceneDescription] = useState(panel.scene_description || '');
  const [dialogue, setDialogue] = useState<DialogueItem[]>(panel.dialogue || []);
  const [saving, setSaving] = useState(false);
  const [busyRegen, setBusyRegen] = useState(false);

  const handleAddDialogue = () => {
    setDialogue([...dialogue, { speaker: panel.speaker || 'Hero', text: '', emotion: 'neutral', bubble_type: 'speech' }]);
  };

  const handleUpdateDialogue = (index: number, field: keyof DialogueItem, value: string) => {
    const updated = [...dialogue];
    updated[index] = { ...updated[index], [field]: value };
    setDialogue(updated);
  };

  const handleRemoveDialogue = (index: number) => {
    setDialogue(dialogue.filter((_, idx) => idx !== index));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await onSave(panel.id, {
        title,
        narration,
        sound_effect: soundEffect,
        image_prompt: imagePrompt,
        scene_description: sceneDescription,
        dialogue
      });
      onClose();
    } catch (e) {
      console.error(e);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-3xl shadow-2xl overflow-hidden flex flex-col my-8 max-h-[90vh]">
        {/* Header */}
        <div className="px-6 py-4 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="comic-title text-2xl text-sky-400">PANEL #{panel.panel_number} EDITOR</span>
          </div>
          <button onClick={onClose} className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form Body */}
        <div className="p-6 space-y-6 overflow-y-auto flex-1">
          {/* Panel Title */}
          <div>
            <label className="block text-xs font-semibold uppercase text-slate-400 mb-1">Panel Title</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-sky-500"
              placeholder="e.g. The Discovery"
            />
          </div>

          {/* Narration Caption */}
          <div>
            <label className="block text-xs font-semibold uppercase text-amber-400 mb-1">Narration Box Text</label>
            <textarea
              rows={2}
              value={narration}
              onChange={(e) => setNarration(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-amber-500"
              placeholder="Narrative text displayed in top yellow caption box..."
            />
          </div>

          {/* Dialogue Speech Bubbles */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-semibold uppercase text-sky-400">Dialogue Speech Bubbles</label>
              <button
                onClick={handleAddDialogue}
                className="flex items-center gap-1 text-xs text-sky-400 hover:text-sky-300 font-medium"
              >
                <Plus className="w-3.5 h-3.5" /> Add Bubble
              </button>
            </div>

            <div className="space-y-3">
              {dialogue.map((item, idx) => (
                <div key={idx} className="p-3 bg-slate-950 border border-slate-800 rounded-xl flex flex-col sm:flex-row items-center gap-2">
                  <input
                    type="text"
                    value={item.speaker}
                    onChange={(e) => handleUpdateDialogue(idx, 'speaker', e.target.value)}
                    placeholder="Speaker"
                    className="w-full sm:w-1/4 bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-white"
                  />
                  <input
                    type="text"
                    value={item.text}
                    onChange={(e) => handleUpdateDialogue(idx, 'text', e.target.value)}
                    placeholder="Speech text..."
                    className="w-full sm:w-1/2 bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-white"
                  />
                  <select
                    value={item.bubble_type || 'speech'}
                    onChange={(e) => handleUpdateDialogue(idx, 'bubble_type', e.target.value)}
                    className="w-full sm:w-1/4 bg-slate-900 border border-slate-800 rounded-lg px-2 py-1.5 text-xs text-white"
                  >
                    <option value="speech">Speech</option>
                    <option value="thought">Thought</option>
                    <option value="shout">Shout</option>
                  </select>
                  <button
                    onClick={() => handleRemoveDialogue(idx)}
                    className="p-1.5 text-slate-500 hover:text-red-400"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Sound Effect */}
          <div>
            <label className="block text-xs font-semibold uppercase text-yellow-400 mb-1">Sound Effect Text</label>
            <input
              type="text"
              value={soundEffect}
              onChange={(e) => setSoundEffect(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-sm text-white"
              placeholder="e.g. WHOOSH, BAM, ROAR"
            />
          </div>

          {/* Image Prompt */}
          <div>
            <label className="block text-xs font-semibold uppercase text-indigo-400 mb-1">Visual Image Prompt</label>
            <textarea
              rows={3}
              value={imagePrompt}
              onChange={(e) => setImagePrompt(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs font-mono text-slate-300 focus:outline-none focus:border-indigo-500"
            />
          </div>
        </div>

        {/* Footer Buttons */}
        <div className="px-6 py-4 bg-slate-950 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <button
              onClick={async () => {
                setBusyRegen(true);
                await onRegenerateImage(panel);
                setBusyRegen(false);
              }}
              disabled={busyRegen}
              className="flex items-center gap-1.5 px-3 py-2 bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-500/30 rounded-xl text-xs font-semibold transition-colors disabled:opacity-50"
            >
              <ImageIcon className="w-4 h-4" />
              <span>Regenerate Image</span>
            </button>

            <button
              onClick={async () => {
                setBusyRegen(true);
                await onRegenerateStory(panel);
                setBusyRegen(false);
              }}
              disabled={busyRegen}
              className="flex items-center gap-1.5 px-3 py-2 bg-amber-600/20 hover:bg-amber-600/30 text-amber-300 border border-amber-500/30 rounded-xl text-xs font-semibold transition-colors disabled:opacity-50"
            >
              <MessageSquare className="w-4 h-4" />
              <span>Regenerate Story</span>
            </button>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              disabled={saving}
              className="flex items-center gap-1.5 px-5 py-2 bg-sky-500 hover:bg-sky-400 text-white rounded-xl text-xs font-semibold shadow-lg shadow-sky-500/20 transition-colors disabled:opacity-50"
            >
              {saving ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
              <span>Save Panel</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
