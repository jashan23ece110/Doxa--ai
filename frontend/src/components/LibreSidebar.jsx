import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Plus,
  Search,
  MessageSquare,
  Trash2,
  Edit2,
  Check,
  PanelLeftClose,
  User,
  ShieldCheck,
  Sparkles,
} from 'lucide-react';
import SvgLogo from '../landing/logo/SvgLogo';

function groupSessionsByDate(sessions = []) {
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();
  const yesterday = today - 86400000;
  const sevenDaysAgo = today - 7 * 86400000;

  const groups = {
    Today: [],
    Yesterday: [],
    'Previous 7 Days': [],
    Older: [],
  };

  sessions.forEach((session) => {
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
  userEmail = 'user@doxa.ai',
}) {
  const [searchQuery, setSearchQuery] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [editTitleText, setEditTitleText] = useState('');

  // Filter sessions by search query
  const filteredSessions = sessions.filter((s) =>
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
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -10 }}
          transition={{ duration: 0.2, ease: 'easeOut' }}
          className="w-full h-full flex flex-col justify-between p-3.5 select-none text-xs font-sans bg-neutral-950/95 backdrop-blur-2xl border-r border-white/[0.08] shadow-2xl relative z-30"
          aria-label="Conversational History Sidebar"
        >
          {/* ── Top Header & Navigation Actions ── */}
          <div className="flex flex-col gap-3.5">
            {/* Sidebar Brand Header */}
            <div className="flex items-center justify-between gap-2 pt-1 pb-2 border-b border-white/[0.08]">
              <div className="flex items-center gap-2.5">
                <div className="p-1.5 rounded-xl bg-white/[0.04] border border-white/[0.1] flex items-center justify-center shadow-inner">
                  <SvgLogo size={18} className="w-4 h-4" />
                </div>
                <span
                  className="font-extrabold text-sm tracking-wider text-white uppercase font-mono"
                  style={{ fontFamily: 'Orbitron, sans-serif' }}
                >
                  DOXA WORKSPACE
                </span>
              </div>

              <button
                type="button"
                onClick={onToggleSidebar}
                className="p-1.5 rounded-xl bg-white/[0.03] hover:bg-white/[0.08] border border-white/[0.1] text-neutral-400 hover:text-white transition-colors cursor-pointer"
                title="Collapse Sidebar"
                aria-label="Collapse Sidebar"
              >
                <PanelLeftClose className="w-4 h-4" />
              </button>
            </div>

            {/* Prominent New Conversation CTA Button */}
            <button
              type="button"
              onClick={onNewSession}
              className="group relative w-full py-2.5 px-4 rounded-xl text-white font-semibold flex items-center justify-center gap-2 hover:brightness-110 active:scale-[0.98] transition-all shadow-[0_0_20px_rgba(124,58,237,0.35)] tracking-wider uppercase text-xs cursor-pointer overflow-hidden border border-white/[0.15]"
              style={{
                background: 'linear-gradient(135deg, #7c3aed 0%, #6366f1 50%, #06b6d4 100%)',
                fontFamily: 'Orbitron, sans-serif',
              }}
            >
              <Plus className="w-4 h-4 stroke-[2.5] group-hover:rotate-90 transition-transform duration-300" />
              <span>New Conversation</span>
            </button>

            {/* Search Input Filter */}
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-neutral-500" />
              <input
                type="text"
                placeholder="Search conversations..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-3 py-2 rounded-xl bg-white/[0.03] border border-white/[0.08] text-neutral-200 placeholder-neutral-500 focus:outline-none focus:border-violet-500/40 text-xs font-sans transition-all"
              />
            </div>
          </div>

          {/* ── Middle Stream: Grouped Conversation History Items ── */}
          <div className="flex-1 overflow-y-auto hud-scrollbar my-3 pr-1 flex flex-col gap-4">
            {Object.entries(grouped).map(([groupTitle, sessionList]) => {
              if (sessionList.length === 0) return null;
              return (
                <div key={groupTitle} className="flex flex-col gap-1">
                  <div
                    className="text-[10px] font-bold uppercase tracking-wider text-neutral-400 px-2 py-1 select-none font-mono flex items-center justify-between"
                    style={{ fontFamily: 'Orbitron, sans-serif' }}
                  >
                    <span>{groupTitle}</span>
                    <span className="text-[9px] text-neutral-400 font-normal">({sessionList.length})</span>
                  </div>

                  {sessionList.map((s) => {
                    const isActive = s.id === currentSessionId;
                    const isEditing = editingId === s.id;

                    return (
                      <div
                        key={s.id}
                        onClick={() => onSelectSession(s.id)}
                        className={`group relative flex items-center justify-between px-3 py-2.5 rounded-xl cursor-pointer border transition-all duration-150 ${
                          isActive
                            ? 'bg-violet-500/15 border-violet-400/35 text-white font-medium shadow-[0_0_12px_rgba(124,58,237,0.2)]'
                            : 'bg-white/[0.02] border-transparent text-neutral-400 hover:text-white hover:bg-white/[0.06] hover:border-white/[0.08]'
                        }`}
                      >
                        <div className="flex items-center gap-2.5 min-w-0 flex-1">
                          {isActive && <span className="w-1 h-3.5 bg-cyan-400 rounded-full shrink-0" />}
                          <MessageSquare
                            className={`w-3.5 h-3.5 shrink-0 ${
                              isActive ? 'text-cyan-400' : 'text-neutral-500 group-hover:text-neutral-300'
                            }`}
                          />

                          {isEditing ? (
                            <input
                              type="text"
                              autoFocus
                              value={editTitleText}
                              onChange={(e) => setEditTitleText(e.target.value)}
                              onKeyDown={(e) => e.key === 'Enter' && handleSaveRename(s.id, e)}
                              onClick={(e) => e.stopPropagation()}
                              className="w-full bg-neutral-900 px-2 py-1 rounded border border-violet-400 text-white font-sans text-xs focus:outline-none"
                            />
                          ) : (
                            <span
                              className="truncate font-sans text-xs text-neutral-200 group-hover:text-white"
                              title={s.title || 'New Conversation'}
                            >
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
                              className="p-1 text-emerald-400 hover:bg-emerald-500/20 rounded-md transition-colors"
                              title="Save title"
                            >
                              <Check className="w-3.5 h-3.5" />
                            </button>
                          ) : (
                            <>
                              <button
                                type="button"
                                onClick={(e) => handleStartRename(s, e)}
                                className="p-1 text-neutral-400 hover:text-white hover:bg-white/10 rounded-md transition-colors"
                                title="Rename conversation"
                              >
                                <Edit2 className="w-3.5 h-3.5" />
                              </button>
                              {sessions.length > 1 && (
                                <button
                                  type="button"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    onDeleteSession(s.id);
                                  }}
                                  className="p-1 text-neutral-400 hover:text-red-400 hover:bg-red-500/20 rounded-md transition-colors"
                                  title="Delete conversation"
                                >
                                  <Trash2 className="w-3.5 h-3.5" />
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

          {/* ── Bottom Profile & Enterprise Account Footer ── */}
          <div className="pt-3 border-t border-white/[0.08] flex items-center justify-between">
            <div className="flex items-center gap-2.5 min-w-0">
              <div className="w-8 h-8 rounded-full bg-white/[0.05] border border-white/[0.12] flex items-center justify-center text-neutral-300 shrink-0 shadow-inner">
                <User className="w-4 h-4 text-cyan-400" />
              </div>
              <div className="flex flex-col min-w-0">
                <span className="text-xs font-medium text-white truncate">{userEmail}</span>
                <span className="text-[10px] text-violet-300 font-mono flex items-center gap-1">
                  <ShieldCheck className="w-3 h-3 text-cyan-400" /> PRO ENGINE
                </span>
              </div>
            </div>
          </div>
        </motion.aside>
      )}
    </AnimatePresence>
  );
}
