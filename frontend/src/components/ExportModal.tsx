import React, { useState } from 'react';
import { X, FileText, Image as ImageIcon, Download, Loader2 } from 'lucide-react';
import { api } from '../services/api';

interface ExportModalProps {
  projectId: string;
  projectTitle: string;
  onClose: () => void;
}

export const ExportModal: React.FC<ExportModalProps> = ({ projectId, projectTitle, onClose }) => {
  const [loadingPdf, setLoadingPdf] = useState(false);
  const [loadingPng, setLoadingPng] = useState(false);
  const [downloadLinks, setDownloadLinks] = useState<{ label: string; url: string }[]>([]);

  const handleExportPDF = async () => {
    setLoadingPdf(true);
    try {
      const res = await api.exportPDF(projectId);
      setDownloadLinks(prev => [...prev, { label: `Download PDF: ${res.filename}`, url: res.download_url }]);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingPdf(false);
    }
  };

  const handleExportPNG = async () => {
    setLoadingPng(true);
    try {
      const res = await api.exportPNG(projectId);
      const newLinks = res.pages.map(p => ({ label: `Download PNG Page: ${p.filename}`, url: p.download_url }));
      setDownloadLinks(prev => [...prev, ...newLinks]);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingPng(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl w-full max-w-md p-6 shadow-2xl overflow-hidden relative">
        <button onClick={onClose} className="absolute top-4 right-4 p-1.5 text-slate-400 hover:text-white rounded-lg">
          <X className="w-5 h-5" />
        </button>

        <h2 className="comic-title text-2xl text-white mb-1">EXPORT COMIC</h2>
        <p className="text-slate-400 text-xs mb-6">Download high-resolution PDF or PNG pages for "{projectTitle}"</p>

        <div className="space-y-4 mb-6">
          <button
            onClick={handleExportPDF}
            disabled={loadingPdf}
            className="w-full flex items-center justify-between p-4 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-2xl transition-colors text-left group disabled:opacity-50"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-red-500/10 text-red-400 flex items-center justify-center">
                <FileText className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-semibold text-white">Export PDF Comic Book</h4>
                <p className="text-xs text-slate-500">Includes cover page & complete page layout</p>
              </div>
            </div>
            {loadingPdf ? <Loader2 className="w-5 h-5 animate-spin text-sky-400" /> : <Download className="w-5 h-5 text-slate-500 group-hover:text-sky-400" />}
          </button>

          <button
            onClick={handleExportPNG}
            disabled={loadingPng}
            className="w-full flex items-center justify-between p-4 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-2xl transition-colors text-left group disabled:opacity-50"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-sky-500/10 text-sky-400 flex items-center justify-center">
                <ImageIcon className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-semibold text-white">Export PNG Comic Pages</h4>
                <p className="text-xs text-slate-500">Rendered composite PNG images per page</p>
              </div>
            </div>
            {loadingPng ? <Loader2 className="w-5 h-5 animate-spin text-sky-400" /> : <Download className="w-5 h-5 text-slate-500 group-hover:text-sky-400" />}
          </button>
        </div>

        {downloadLinks.length > 0 && (
          <div className="p-4 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
            <h5 className="text-xs font-semibold uppercase text-emerald-400 mb-2">Generated Exports Ready:</h5>
            {downloadLinks.map((link, idx) => (
              <a
                key={idx}
                href={link.url}
                download
                className="flex items-center gap-2 text-xs font-medium text-sky-400 hover:underline py-1 block truncate"
              >
                <Download className="w-3.5 h-3.5 shrink-0" />
                <span className="truncate">{link.label}</span>
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
