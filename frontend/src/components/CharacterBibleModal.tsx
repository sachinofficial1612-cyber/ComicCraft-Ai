import React from 'react';
import { Character } from '../types/comic';
import { X, User, Shield, Palette, Shirt } from 'lucide-react';

interface CharacterBibleModalProps {
  characters: Character[];
  onClose: () => void;
}

export const CharacterBibleModal: React.FC<CharacterBibleModalProps> = ({ characters, onClose }) => {
  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl w-full max-w-2xl p-6 shadow-2xl overflow-hidden relative max-h-[85vh] flex flex-col">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div>
            <h2 className="comic-title text-2xl text-sky-400">CHARACTER BIBLE</h2>
            <p className="text-xs text-slate-400">Visual specs maintained for panel image consistency</p>
          </div>
          <button onClick={onClose} className="p-1.5 text-slate-400 hover:text-white rounded-lg">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-4 overflow-y-auto space-y-6 flex-1">
          {characters.map((char) => (
            <div key={char.id} className="bg-slate-950 border border-slate-800 rounded-2xl p-5 space-y-3">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-sky-500/20 text-sky-400 flex items-center justify-center font-bold text-lg">
                  {char.name[0]}
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white">{char.name}</h3>
                  <p className="text-xs text-slate-400">{char.description}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 text-xs">
                <div className="p-3 bg-slate-900 rounded-xl border border-slate-800">
                  <span className="font-semibold text-sky-400 block mb-1 flex items-center gap-1">
                    <User className="w-3.5 h-3.5" /> Appearance
                  </span>
                  <p className="text-slate-300">{char.appearance || 'Not specified'}</p>
                </div>

                <div className="p-3 bg-slate-900 rounded-xl border border-slate-800">
                  <span className="font-semibold text-emerald-400 block mb-1 flex items-center gap-1">
                    <Shirt className="w-3.5 h-3.5" /> Clothing
                  </span>
                  <p className="text-slate-300">{char.clothing || 'Not specified'}</p>
                </div>

                <div className="p-3 bg-slate-900 rounded-xl border border-slate-800">
                  <span className="font-semibold text-amber-400 block mb-1 flex items-center gap-1">
                    <Palette className="w-3.5 h-3.5" /> Signature Colors
                  </span>
                  <p className="text-slate-300">{char.colors || 'Not specified'}</p>
                </div>

                <div className="p-3 bg-slate-900 rounded-xl border border-slate-800">
                  <span className="font-semibold text-purple-400 block mb-1 flex items-center gap-1">
                    <Shield className="w-3.5 h-3.5" /> Personality
                  </span>
                  <p className="text-slate-300">{char.personality || 'Not specified'}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
