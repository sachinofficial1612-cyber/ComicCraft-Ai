import React from 'react';
import { AlertCircle, CheckCircle, Info, X } from 'lucide-react';

export interface ToastProps {
  message: string;
  type?: 'success' | 'error' | 'info';
  onClose: () => void;
}

export const Toast: React.FC<ToastProps> = ({ message, type = 'info', onClose }) => {
  const bg = type === 'success' ? 'bg-emerald-900/90 border-emerald-500 text-emerald-100' :
             type === 'error' ? 'bg-red-900/90 border-red-500 text-red-100' :
             'bg-sky-900/90 border-sky-500 text-sky-100';

  const Icon = type === 'success' ? CheckCircle : type === 'error' ? AlertCircle : Info;

  return (
    <div className={`fixed bottom-6 right-6 z-50 flex items-center gap-3 px-4 py-3 rounded-xl border shadow-2xl backdrop-blur-md transition-all ${bg}`}>
      <Icon className="w-5 h-5 shrink-0" />
      <span className="text-sm font-medium">{message}</span>
      <button onClick={onClose} className="p-1 hover:bg-white/10 rounded-lg">
        <X className="w-4 h-4" />
      </button>
    </div>
  );
};
