import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Plus, 
  Search, 
  MessageSquare, 
  Trash2, 
  Edit2, 
  Check, 
  X, 
  Bot, 
  LogOut, 
  Shield,
  PanelLeftClose,
  User,
  ShieldCheck
} from 'lucide-react';
import doxaLogo from '../assets/logo.png';

function groupSessionsByDate(sessions = []) {
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();
  const yesterday = today - 86400000;
  const sevenDaysAgo = today - 7 * 86400000;

  const groups = {
    Today: [],
    Yesterday: [],
    'Previous 7 Days': [],
    Older: []
  };

  sessions.forEach(session => {
    const sDate = new Date(session.timestamp || session.createdAt || Date.now()).getTime();
    if (sDate >= today) {
      groups.Today.push(session);
    } else if (sDate >= yesterday) {
      groups.Yesterday.push(session);
    } else if (sDate >= sevenDaysAgo) {
      groups['Previous 7 Days'].push(session);
    } else {
      groups.Older.push(session);
    }
  });

  return groups;
}

export default function LibreSidebar({
  sessions = [],
  currentSessionId,
  onSelectSession,
  onNewSession,
  onDeleteSession,
  onRenameSession,
  isOpen,
  onToggleSidebar,
  userEmail = 'user@doxa.ai'
}) {
  const [searchQuery, setSearchQuery] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [editTitleText, setEditTitleText] = useState('');

  // Filter sessions by search query
  const filteredSessions = sessions.filter(s => 
    (s.title || 'New Conversation').toLowerCase().includes(searchQuery.toLowerCase())
  );

  const grouped = groupSessionsByDate(filteredSessions);

  const handleStartRename = (s, e) => {
    e.stopPropagation();
    setEditingId(s.id);
    setEditTitleText(s.title || 'New Conversation');
  };

  const handleSaveRename = (sId, e) => {
    e.stopPropagation();
    if (editTitleText.trim() && onRenameSession) {
      onRenameSession(sId, editTitleText.trim());
    }
    setEditingId(null);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.aside
          initial={{ x: -280, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: -280, opacity: 0 }}
          transition={{ duration: 0.25, ease: 'easeOut' }}
          className="fixed top-0 left-0 bottom-0 z-40 w-72 bg-black/90 backdrop-blur-2xl border-r border-[var(--jarvis-accent)]/15 flex flex-col justify-between p-3 select-none text-xs font-mono shadow-2xl"
        >
          {/* Top Section */}
          <div className="flex flex-col gap-3">
            {/* Sidebar Header & New Chat Button */}
            <div className="flex items-center justify-between gap-2 pt-1 pb-1 border-b border-[var(--jarvis-accent)]/10">
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-lg bg-[var(--jarvis-accent)]/15 border border-[var(--jarvis-accent)]/30 flex items-center justify-center p-1 overflow-hidden">
                  <img
                    src={doxaLogo}
                    alt="Doxa Logo"
                    className="w-full h-full object-contain filter invert brightness-200"
                  />
                </div>
                <span className="font-bold text-white tracking-widest uppercase font-orbitron text-sm">
                  DOXA AI
                </span>
              </div>

              <button
                type="button"
                onClick={onToggleSidebar}
                className="p-1.5 rounded-lg border border-neutral-800 text-neutral-400 hover:text-white hover:bg-neutral-800 transition-colors"
                title="Collapse Sidebar"
              >
                <PanelLeftClose className="w-4 h-4" />
              </button>
            </div>

            {/* Prominent New Chat Button */}
            <button
              type="button"
              onClick={onNewSession}
              className="w-full py-2.5 px-4 rounded-xl bg-[var(--jarvis-accent)] text-black font-bold flex items-center justify-center gap-2 hover:brightness-110 active:scale-[0.98] transition-all shadow-[0_0_15px_rgba(var(--jarvis-accent-rgb),0.3)] tracking-wider uppercase text-xs"
            >
              <Plus className="w-4 h-4 stroke-[2.5]" />
              <span>New Conversation</span>
            </button>

            {/* Search Input */}
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-neutral-500" />
              <input
                type="text"
                placeholder="Search chats..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-3 py-1.5 rounded-lg bg-neutral-900/80 border border-neutral-800 text-[#e0d6c2] placeholder-neutral-500 focus:outline-none focus:border-[var(--jarvis-accent)]/40 text-xs font-sans transition-colors"
              />
            </div>
          </div>

          {/* Middle Section: Grouped Conversations List */}
          <div className="flex-1 overflow-y-auto hud-scrollbar my-3 pr-1 flex flex-col gap-4">
            {Object.entries(grouped).map(([groupTitle, sessionList]) => {
              if (sessionList.length === 0) return null;
              return (
                <div key={groupTitle} className="flex flex-col gap-1">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-[#7a7060] px-2 py-0.5 select-none">
                    {groupTitle}
                  </div>

                  {sessionList.map(s => {
                    const isActive = s.id === currentSessionId;
                    const isEditing = editingId === s.id;

                    return (
                      <div
                        key={s.id}
                        onClick={() => onSelectSession(s.id)}
                        className={`group relative flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer border transition-all duration-150 ${
                          isActive
                            ? 'bg-[var(--jarvis-accent)]/15 border-[var(--jarvis-accent)]/30 text-[var(--jarvis-accent)] font-semibold shadow-[0_0_10px_rgba(var(--jarvis-accent-rgb),0.1)]'
                            : 'bg-neutral-900/40 border-transparent text-neutral-400 hover:text-[#e0d6c2] hover:bg-neutral-900/80 hover:border-neutral-800'
                        }`}
                      >
                        <div className="flex items-center gap-2 min-w-0 flex-1">
                          <MessageSquare className={`w-3.5 h-3.5 shrink-0 ${isActive ? 'text-[var(--jarvis-accent)]' : 'text-neutral-500'}`} />
                          
                          {isEditing ? (
                            <input
                              type="text"
                              autoFocus
                              value={editTitleText}
                              onChange={(e) => setEditTitleText(e.target.value)}
                              onKeyDown={(e) => e.key === 'Enter' && handleSaveRename(s.id, e)}
                              onClick={(e) => e.stopPropagation()}
                              className="w-full bg-black px-1.5 py-0.5 rounded border border-[var(--jarvis-accent)]/40 text-white font-sans text-xs focus:outline-none"
                            />
                          ) : (
                            <span className="truncate font-sans text-xs" title={s.title || 'New Conversation'}>
                              {s.title || 'New Conversation'}
                            </span>
                          )}
                        </div>

                        {/* Action Buttons (Rename & Delete) */}
                        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity shrink-0 ml-1">
                          {isEditing ? (
                            <button
                              type="button"
                              onClick={(e) => handleSaveRename(s.id, e)}
                              className="p-1 text-emerald-400 hover:bg-emerald-500/20 rounded"
                            >
                              <Check className="w-3 h-3" />
                            </button>
                          ) : (
                            <>
                              <button
                                type="button"
                                onClick={(e) => handleStartRename(s, e)}
                                className="p-1 text-neutral-400 hover:text-white hover:bg-neutral-800 rounded"
                                title="Rename"
                              >
                                <Edit2 className="w-3 h-3" />
                              </button>
                              {sessions.length > 1 && (
                                <button
                                  type="button"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    onDeleteSession(s.id);
                                  }}
                                  className="p-1 text-neutral-400 hover:text-red-400 hover:bg-red-500/20 rounded"
                                  title="Delete"
                                >
                                  <Trash2 className="w-3 h-3" />
                                </button>
                              )}
                            </>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              );
            })}
          </div>

          {/* Bottom Profile / Status Footer */}
          <div className="pt-3 border-t border-[var(--jarvis-accent)]/10 flex items-center justify-between">
            <div className="flex items-center gap-2 min-w-0">
              <div className="w-7 h-7 rounded-full bg-neutral-800 border border-neutral-700 flex items-center justify-center text-neutral-300 shrink-0">
                <User className="w-3.5 h-3.5" />
              </div>
              <div className="flex flex-col min-w-0">
                <span className="text-[11px] font-semibold text-white truncate">{userEmail}</span>
                <span className="text-[9px] text-[var(--jarvis-accent)] font-mono flex items-center gap-1">
                  <ShieldCheck className="w-2.5 h-2.5" /> PRO ENGINE
                </span>
              </div>
            </div>
          </div>
        </motion.aside>
      )}
    </AnimatePresence>
  );
}
