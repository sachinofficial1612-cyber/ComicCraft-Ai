import { Project, CreateProjectPayload, Panel, GenerationStatus } from '../types/comic';

const API_BASE = '/api';

async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, options);
  if (!res.ok) {
    let errorMsg = `HTTP Error ${res.status}`;
    try {
      const errorData = await res.json();
      errorMsg = errorData.detail || errorData.error || errorMsg;
    } catch {
      // fallback to status text
    }
    throw new Error(errorMsg);
  }
  return res.json();
}

export const api = {
  // Health
  getHealth: () => fetchJSON<{ status: string; gemini_configured: boolean }>(`${API_BASE}/health`),
  getAIHealth: () => fetchJSON<{ configured: boolean; text_model: string; image_model: string }>(`${API_BASE}/health/ai`),

  // Projects
  createProject: (payload: CreateProjectPayload) =>
    fetchJSON<Project>(`${API_BASE}/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }),

  listProjects: () => fetchJSON<Project[]>(`${API_BASE}/projects`),

  getProject: (id: string) => fetchJSON<Project>(`${API_BASE}/projects/${id}`),

  getDemoProject: () => fetchJSON<Project>(`${API_BASE}/projects/demo`, { method: 'POST' }),

  updateProject: (id: string, updates: Partial<Project>) =>
    fetchJSON<Project>(`${API_BASE}/projects/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    }),

  deleteProject: (id: string) =>
    fetch(`${API_BASE}/projects/${id}`, { method: 'DELETE' }),

  generateComic: (id: string) =>
    fetchJSON<Project>(`${API_BASE}/projects/${id}/generate`, { method: 'POST' }),

  getProjectStatus: (id: string) =>
    fetchJSON<GenerationStatus>(`${API_BASE}/projects/${id}/status`),

  // Panels
  updatePanel: (projectId: string, panelId: string, updates: Partial<Panel>) =>
    fetchJSON<Panel>(`${API_BASE}/projects/${projectId}/panels/${panelId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    }),

  regeneratePanelImage: (projectId: string, panelId: string) =>
    fetchJSON<Panel>(`${API_BASE}/projects/${projectId}/panels/${panelId}/regenerate-image`, { method: 'POST' }),

  regeneratePanelStory: (projectId: string, panelId: string) =>
    fetchJSON<Panel>(`${API_BASE}/projects/${projectId}/panels/${panelId}/regenerate-story`, { method: 'POST' }),

  regeneratePanelBoth: (projectId: string, panelId: string) =>
    fetchJSON<Panel>(`${API_BASE}/projects/${projectId}/panels/${panelId}/regenerate-both`, { method: 'POST' }),

  deletePanel: (projectId: string, panelId: string) =>
    fetchJSON<{ message: string; remaining_panels: number }>(`${API_BASE}/projects/${projectId}/panels/${panelId}`, { method: 'DELETE' }),

  addPanel: (projectId: string) =>
    fetchJSON<Panel>(`${API_BASE}/projects/${projectId}/panels`, { method: 'POST' }),

  // Exports
  exportPDF: (projectId: string) =>
    fetchJSON<{ download_url: string; filename: string }>(`${API_BASE}/projects/${projectId}/export/pdf`, { method: 'POST' }),

  exportPNG: (projectId: string) =>
    fetchJSON<{ pages: { download_url: string; filename: string }[] }>(`${API_BASE}/projects/${projectId}/export/png`, { method: 'POST' }),
};
