import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Wand2, Lightbulb, ArrowRight, Loader2 } from 'lucide-react';
import { api } from '../services/api';
import { GenerationProgress } from '../components/GenerationProgress';
import { GenerationStatus } from '../types/comic';

export const CreateComicPage: React.FC = () => {
  const navigate = useNavigate();

  const [prompt, setPrompt] = useState('');
  const [characterName, setCharacterName] = useState('Free');
  const [setting, setSetting] = useState('Enchanted Forest');
  const [tone, setTone] = useState('Dramatic');
  const [artStyle, setArtStyle] = useState('Realistic');
  const [panelCount, setPanelCount] = useState('6');
  
  const [isGenerating, setIsGenerating] = useState(false);
  const [genStatus, setGenStatus] = useState<GenerationStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  const presets = [
    { title: "Free the Fox", prompt: "A brave red fox named Free explores an enchanted forest, discovering glowing ancient ruins and unlocking mystical secrets.", character: "Free", setting: "Enchanted Forest", tone: "Dramatic", style: "Realistic" },
    { title: "Chrono Scientist", prompt: "A brilliant young scientist invents a pocket device that can pause time for 60 seconds, but discovers she isn't the only one moving.", character: "Elena", setting: "Metropolis Lab", tone: "Sci-Fi", style: "Cinematic" },
    { title: "Rover Mars", prompt: "A lone survivor maintenance robot stranded on Mars builds a high-power beacon signal to contact Earth.", character: "Unit-7", setting: "Martian Crater", tone: "Emotional", style: "3D" }
  ];

  const handleApplyPreset = (p: typeof presets[0]) => {
    setPrompt(p.prompt);
    setCharacterName(p.character);
    setSetting(p.setting);
    setTone(p.tone);
    setArtStyle(p.style);
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setIsGenerating(true);
    setError(null);
    setGenStatus({ project_id: '', status: 'generating', completed_panels: 0, total_panels: parseInt(panelCount) || 6, progress_percentage: 10 });

    try {
      // Step 1: Create Draft Project
      const project = await api.createProject({
        original_prompt: prompt,
        character_name: characterName,
        setting: setting,
        tone: tone,
        art_style: artStyle,
        panel_count: panelCount
      });

      // Step 2: Trigger AI Generation Pipeline
      setGenStatus(prev => prev ? { ...prev, project_id: project.id, progress_percentage: 25 } : null);

      const completedProject = await api.generateComic(project.id);

      if (completedProject.status === 'failed') {
        throw new Error(completedProject.error_message || 'Comic generation failed');
      }

      setGenStatus(prev => prev ? { ...prev, progress_percentage: 100 } : null);
      
      // Navigate to comic preview page
      navigate(`/comic/${completedProject.id}`);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'An error occurred during generation.');
      setIsGenerating(false);
    }
  };

  if (isGenerating) {
    return <GenerationProgress status={genStatus} error={error} />;
  }

  return (
    <div className="max-w-4xl mx-auto py-8">
      <div className="text-center mb-10 space-y-2">
        <h1 className="comic-title text-4xl sm:text-5xl text-white">CREATE YOUR COMIC</h1>
        <p className="text-slate-400 text-sm">Enter your story idea and customize character, setting, and visual style.</p>
      </div>

      {/* Preset Examples */}
      <div className="mb-8 p-4 bg-slate-900/60 border border-slate-800 rounded-2xl">
        <div className="flex items-center gap-2 text-amber-400 text-xs font-semibold uppercase tracking-wider mb-3">
          <Lightbulb className="w-4 h-4" /> Try An Example Story Prompt
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {presets.map((p, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleApplyPreset(p)}
              className="p-3 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl text-left transition-colors group"
            >
              <h4 className="text-xs font-bold text-white group-hover:text-sky-400">{p.title}</h4>
              <p className="text-[11px] text-slate-400 line-clamp-2 mt-1">{p.prompt}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Generation Form */}
      <form onSubmit={handleGenerate} className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl space-y-6">
        {/* Story Idea */}
        <div>
          <label className="block text-xs font-extrabold uppercase text-sky-400 mb-2">
            Story Idea / Concept <span className="text-red-400">*</span>
          </label>
          <textarea
            rows={4}
            required
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-2xl p-4 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-sky-500 transition-colors"
            placeholder="Write your story prompt (e.g. A brave red fox named Free explores an enchanted forest, discovering glowing ancient ruins...)"
          />
        </div>

        {/* Character & Setting */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label className="block text-xs font-extrabold uppercase text-slate-300 mb-2">Main Character Name</label>
            <input
              type="text"
              required
              value={characterName}
              onChange={(e) => setCharacterName(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-sky-500"
            />
          </div>

          <div>
            <label className="block text-xs font-extrabold uppercase text-slate-300 mb-2">Primary Setting</label>
            <input
              type="text"
              required
              value={setting}
              onChange={(e) => setSetting(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-sky-500"
            />
          </div>
        </div>

        {/* Tone, Art Style & Panel Count */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div>
            <label className="block text-xs font-extrabold uppercase text-slate-300 mb-2">Story Tone</label>
            <select
              value={tone}
              onChange={(e) => setTone(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-sky-500"
            >
              <option value="Dramatic">Dramatic</option>
              <option value="Humorous">Humorous</option>
              <option value="Action-Packed">Action-Packed</option>
              <option value="Mystical">Mystical</option>
              <option value="Sci-Fi">Sci-Fi</option>
              <option value="Dark">Dark</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-extrabold uppercase text-slate-300 mb-2">Art Style</label>
            <select
              value={artStyle}
              onChange={(e) => setArtStyle(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-sky-500"
            >
              <option value="Realistic">Realistic</option>
              <option value="Cartoon">Cartoon</option>
              <option value="Anime">Anime</option>
              <option value="Manga">Manga</option>
              <option value="Watercolor">Watercolor</option>
              <option value="Cinematic">Cinematic</option>
              <option value="3D">3D</option>
              <option value="Comic Book">Comic Book</option>
              <option value="Noir">Noir</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-extrabold uppercase text-slate-300 mb-2">Panel Count</label>
            <select
              value={panelCount}
              onChange={(e) => setPanelCount(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-sky-500"
            >
              <option value="4">4 Panels (2×2)</option>
              <option value="6">6 Panels (2×3)</option>
              <option value="8">8 Panels (Sequential)</option>
              <option value="10">10 Panels (Multi-Page)</option>
              <option value="AUTO">AUTO (AI Decides)</option>
            </select>
          </div>
        </div>

        {/* Submit CTA */}
        <button
          type="submit"
          className="w-full flex items-center justify-center gap-2 py-4 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-lg rounded-2xl shadow-xl shadow-sky-500/25 transition-all transform hover:-translate-y-0.5"
        >
          <Wand2 className="w-5 h-5" />
          <span>Generate AI Comic</span>
        </button>
      </form>
    </div>
  );
};
