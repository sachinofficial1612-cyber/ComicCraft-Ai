import React from 'react';

export const ErrorState: React.FC<{ title?: string; message: string; onRetry?: () => void }> = ({
  title = 'Something went wrong',
  message,
  onRetry
}) => (
  <div className="flex flex-col items-center justify-center min-h-[300px] p-8 text-center bg-slate-900/50 rounded-2xl border border-red-500/20 max-w-lg mx-auto">
    <div className="w-12 h-12 rounded-full bg-red-500/10 text-red-400 flex items-center justify-center mb-4 text-xl">
      ⚠️
    </div>
    <h3 className="text-xl font-bold text-slate-100 mb-2">{title}</h3>
    <p className="text-slate-400 text-sm mb-6">{message}</p>
    {onRetry && (
      <button
        onClick={onRetry}
        className="px-5 py-2.5 bg-sky-500 hover:bg-sky-400 text-white font-semibold text-sm rounded-xl transition-colors shadow-lg shadow-sky-500/20"
      >
        Try Again
      </button>
    )}
  </div>
);
