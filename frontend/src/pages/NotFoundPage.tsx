import React from 'react';
import { Link } from 'react-router-dom';
import { Home } from 'lucide-react';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center text-center p-8">
      <h1 className="comic-title text-8xl text-sky-400 mb-2">404</h1>
      <h2 className="text-2xl font-bold text-white mb-4">Comic Panel Not Found</h2>
      <p className="text-slate-400 text-sm max-w-md mb-8">The story page you are looking for doesn't exist or has been moved.</p>
      <Link
        to="/"
        className="flex items-center gap-2 px-6 py-3 bg-sky-500 hover:bg-sky-400 text-white font-bold text-sm rounded-xl transition-all shadow-lg shadow-sky-500/20"
      >
        <Home className="w-4 h-4" />
        <span>Return to Home</span>
      </Link>
    </div>
  );
};
