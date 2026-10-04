import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Project } from '../types/comic';
import { api } from '../services/api';
import { LoadingState } from '../components/LoadingState';
import { ErrorState } from '../components/ErrorState';
import { PlusCircle, BookOpen, Trash2, ExternalLink, Calendar, Layers, Image as ImageIcon } from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProjects = async () => {
    try {
      const data = await api.listProjects();
      setProjects(data);
    } catch (e: any) {
      setError(e.message || 'Failed to load projects shelf');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleDelete = async (id: string, title: string) => {
    if (!window.confirm(`Are you sure you want to delete "${title}"?`)) return;
    try {
      await api.deleteProject(id);
      setProjects(prev => prev.filter(p => p.id !== id));
    } catch (e: any) {
      alert(`Delete failed: ${e.message}`);
    }
  };

  if (loading) return <LoadingState message="Loading your comic shelf..." />;
  if (error) return <ErrorState message={error} onRetry={fetchProjects} />;

  return (
    <div className="max-w-7xl mx-auto py-8 space-y-8">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="comic-title text-4xl text-white">YOUR COMIC SHELF</h1>
          <p className="text-slate-400 text-sm">Manage, edit, and export your AI-created comic stories.</p>
        </div>

        <Link
          to="/create"
          className="flex items-center gap-2 px-5 py-2.5 bg-sky-500 hover:bg-sky-400 text-white font-bold text-sm rounded-xl shadow-lg shadow-sky-500/20 transition-all"
        >
          <PlusCircle className="w-4 h-4" />
          <span>Create New Comic</span>
        </Link>
      </div>

      {projects.length === 0 ? (
        <div className="text-center py-20 bg-slate-900/40 border border-slate-800 rounded-3xl p-8 max-w-lg mx-auto space-y-4">
          <BookOpen className="w-12 h-12 text-slate-600 mx-auto" />
          <h3 className="text-xl font-bold text-white">Your comic shelf is empty</h3>
          <p className="text-slate-400 text-sm">Start your creative journey by turning any story prompt into a complete illustrated comic book!</p>
          <Link
            to="/create"
            className="inline-flex items-center gap-2 px-6 py-3 bg-sky-500 hover:bg-sky-400 text-white font-bold text-sm rounded-xl transition-all"
          >
            Create Your First Comic
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((proj) => {
            const firstPanel = proj.panels && proj.panels.length > 0 ? proj.panels[0] : null;
            const createdDate = new Date(proj.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });

            return (
              <div
                key={proj.id}
                className="group bg-slate-900 border-2 border-slate-800 rounded-2xl overflow-hidden hover:border-sky-500/50 shadow-xl transition-all flex flex-col"
              >
                {/* Thumbnail Preview */}
                <div className="relative aspect-[16/9] bg-slate-950 flex items-center justify-center overflow-hidden border-b border-slate-800">
                  {firstPanel?.image_path ? (
                    <img
                      src={firstPanel.image_path}
                      alt={proj.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  ) : (
                    <ImageIcon className="w-10 h-10 text-slate-700" />
                  )}

                  <div className="absolute top-3 right-3 px-2.5 py-1 bg-slate-950/80 backdrop-blur-xs rounded-full border border-slate-800 text-[10px] uppercase font-bold text-sky-400">
                    {proj.art_style}
                  </div>
                </div>

                {/* Card Details */}
                <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
                  <div>
                    <h3 className="text-lg font-bold text-white group-hover:text-sky-400 transition-colors line-clamp-1">
                      {proj.title}
                    </h3>
                    <p className="text-xs text-slate-400 line-clamp-2 mt-1">
                      {proj.original_prompt}
                    </p>
                  </div>

                  <div className="flex items-center justify-between text-xs text-slate-500 pt-2 border-t border-slate-800/60">
                    <span className="flex items-center gap-1">
                      <Layers className="w-3.5 h-3.5 text-sky-400" /> {proj.panels.length || proj.panel_count} Panels
                    </span>
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5" /> {createdDate}
                    </span>
                  </div>
                </div>

                {/* Actions Footer */}
                <div className="px-5 py-3 bg-slate-950 border-t border-slate-800 flex items-center justify-between">
                  <Link
                    to={`/comic/${proj.id}`}
                    className="flex items-center gap-1.5 text-xs font-bold text-sky-400 hover:text-sky-300"
                  >
                    <span>Open Comic</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </Link>

                  <button
                    onClick={() => handleDelete(proj.id, proj.title)}
                    className="p-1.5 text-slate-500 hover:text-red-400 rounded-lg hover:bg-red-500/10 transition-colors"
                    title="Delete Project"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
