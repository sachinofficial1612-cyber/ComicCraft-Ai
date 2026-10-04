import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Project, Panel } from '../types/comic';
import { api } from '../services/api';
import { ComicCanvas } from '../components/ComicCanvas';
import { PanelEditor } from '../components/PanelEditor';
import { ExportModal } from '../components/ExportModal';
import { CharacterBibleModal } from '../components/CharacterBibleModal';
import { LoadingState } from '../components/LoadingState';
import { ErrorState } from '../components/ErrorState';
import { Toast } from '../components/Toast';
import { Edit3, Download, UserCheck, PlusCircle, LayoutGrid, Save, Sparkles } from 'lucide-react';

export const PreviewComicPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [editingPanel, setEditingPanel] = useState<Panel | null>(null);
  const [showExportModal, setShowExportModal] = useState(false);
  const [showBibleModal, setShowBibleModal] = useState(false);
  const [regeneratingPanelId, setRegeneratingPanelId] = useState<string | null>(null);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const fetchProjectData = async () => {
    if (!id) return;
    try {
      const data = await api.getProject(id);
      setProject(data);
    } catch (e: any) {
      setError(e.message || 'Failed to load project');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjectData();
  }, [id]);

  if (loading) return <LoadingState message="Loading your AI comic..." />;
  if (error || !project) return <ErrorState message={error || 'Project not found'} onRetry={fetchProjectData} />;

  const handleSavePanel = async (panelId: string, updates: Partial<Panel>) => {
    if (!project) return;
    try {
      const updatedPanel = await api.updatePanel(project.id, panelId, updates);
      setProject(prev => {
        if (!prev) return prev;
        return {
          ...prev,
          panels: prev.panels.map(p => p.id === panelId ? updatedPanel : p)
        };
      });
      setToastMessage('Panel changes saved!');
    } catch (e: any) {
      setToastMessage(`Error saving: ${e.message}`);
    }
  };

  const handleRegenerateImage = async (panel: Panel) => {
    if (!project) return;
    setRegeneratingPanelId(panel.id);
    try {
      const updated = await api.regeneratePanelImage(project.id, panel.id);
      setProject(prev => prev ? {
        ...prev,
        panels: prev.panels.map(p => p.id === panel.id ? updated : p)
      } : prev);
      setToastMessage(`Artwork regenerated for Panel #${panel.panel_number}`);
    } catch (e: any) {
      setToastMessage(`Regeneration error: ${e.message}`);
    } finally {
      setRegeneratingPanelId(null);
    }
  };

  const handleRegenerateStory = async (panel: Panel) => {
    if (!project) return;
    setRegeneratingPanelId(panel.id);
    try {
      const updated = await api.regeneratePanelStory(project.id, panel.id);
      setProject(prev => prev ? {
        ...prev,
        panels: prev.panels.map(p => p.id === panel.id ? updated : p)
      } : prev);
      setToastMessage(`Dialogue regenerated for Panel #${panel.panel_number}`);
    } catch (e: any) {
      setToastMessage(`Story regeneration error: ${e.message}`);
    } finally {
      setRegeneratingPanelId(null);
    }
  };

  const handleDeletePanel = async (panel: Panel) => {
    if (!project || !window.confirm(`Delete Panel #${panel.panel_number}?`)) return;
    try {
      await api.deletePanel(project.id, panel.id);
      fetchProjectData();
      setToastMessage('Panel deleted');
    } catch (e: any) {
      setToastMessage(`Delete error: ${e.message}`);
    }
  };

  const handleAddPanel = async () => {
    if (!project) return;
    try {
      const newPanel = await api.addPanel(project.id);
      setProject(prev => prev ? { ...prev, panels: [...prev.panels, newPanel] } : prev);
      setToastMessage('New panel added!');
    } catch (e: any) {
      setToastMessage(`Add panel error: ${e.message}`);
    }
  };

  return (
    <div className="max-w-7xl mx-auto py-6 space-y-8">
      {/* Top Action Header Toolbar */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-wrap items-center justify-between gap-4 sticky top-20 z-30 shadow-xl backdrop-blur-md bg-slate-900/95">
        <div className="flex items-center gap-3">
          <Link to="/dashboard" className="p-2 text-slate-400 hover:text-white bg-slate-950 rounded-xl border border-slate-800">
            <LayoutGrid className="w-4 h-4" />
          </Link>
          <div>
            <h2 className="text-base font-bold text-white truncate max-w-xs sm:max-w-md">{project.title}</h2>
            <span className="text-xs text-sky-400 font-medium">{project.art_style} Style • {project.panels.length} Panels</span>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {project.characters.length > 0 && (
            <button
              onClick={() => setShowBibleModal(true)}
              className="flex items-center gap-1.5 px-3.5 py-2 bg-slate-950 hover:bg-slate-800 text-slate-300 rounded-xl text-xs font-semibold border border-slate-800 transition-colors"
            >
              <UserCheck className="w-4 h-4 text-emerald-400" />
              <span>Character Bible</span>
            </button>
          )}

          <button
            onClick={() => setShowExportModal(true)}
            className="flex items-center gap-1.5 px-4 py-2 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-sky-500/20 transition-all"
          >
            <Download className="w-4 h-4" />
            <span>Export Comic</span>
          </button>

          <Link
            to="/create"
            className="flex items-center gap-1.5 px-3.5 py-2 bg-slate-950 hover:bg-slate-800 text-slate-300 rounded-xl text-xs font-semibold border border-slate-800 transition-colors"
          >
            <PlusCircle className="w-4 h-4 text-sky-400" />
            <span>Create New</span>
          </Link>
        </div>
      </div>

      {/* Main Comic Canvas Rendering */}
      <ComicCanvas
        project={project}
        onEditPanel={(p) => setEditingPanel(p)}
        onRegenerateImage={handleRegenerateImage}
        onRegenerateStory={handleRegenerateStory}
        onDeletePanel={handleDeletePanel}
        onAddPanel={handleAddPanel}
        regeneratingPanelId={regeneratingPanelId}
      />

      {/* Panel Editor Modal */}
      {editingPanel && (
        <PanelEditor
          panel={editingPanel}
          onSave={handleSavePanel}
          onClose={() => setEditingPanel(null)}
          onRegenerateImage={handleRegenerateImage}
          onRegenerateStory={handleRegenerateStory}
        />
      )}

      {/* Export Modal */}
      {showExportModal && (
        <ExportModal
          projectId={project.id}
          projectTitle={project.title}
          onClose={() => setShowExportModal(false)}
        />
      )}

      {/* Character Bible Modal */}
      {showBibleModal && (
        <CharacterBibleModal
          characters={project.characters}
          onClose={() => setShowBibleModal(false)}
        />
      )}

      {/* Toast Notification */}
      {toastMessage && (
        <Toast
          message={toastMessage}
          onClose={() => setToastMessage(null)}
        />
      )}
    </div>
  );
};
