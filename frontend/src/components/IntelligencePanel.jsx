import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Cpu,
  Database,
  FileText,
  Plus,
  Trash2,
  Activity,
  Shield,
  Layers,
  ChevronRight,
  Upload,
  Loader2,
  X,
} from 'lucide-react';

export default function IntelligencePanel({
  agentStatus,
  agentLoading = false,
  currentSessionId = '',
  documents = [],
  retrievedContext = [],
  onUploadDoc,
  onDeleteDoc,
  uploadingDoc = false,
  isOpen = true,
  onClose,
}) {
  const [activeTab, setActiveTab] = useState('telemetry'); // 'telemetry' | 'knowledge' | 'documents'

  const currentPhase = (() => {
    if (!agentStatus) return 'IDLE';
    if (agentStatus.status === 'completed') return 'DONE';
    if (agentStatus.status === 'failed') return 'FAILED';
    if (agentStatus.status === 'running') {
      const stepCount = agentStatus.steps?.length || 0;
      if (stepCount <= 1) return 'PLANNING';
      if (stepCount <= 4) return 'EXECUTING';
      return 'REVIEWING';
    }
    return 'IDLE';
  })();

  const stepsCount = agentStatus?.steps?.length || 0;
  const lastStep = agentStatus?.steps?.[stepsCount - 1];

  return (
    <aside
      className="w-full h-full flex flex-col justify-between p-3.5 select-none text-xs font-sans bg-neutral-950/90 backdrop-blur-2xl border-l border-white/[0.08] shadow-2xl overflow-hidden relative z-20"
      aria-label="Intelligence Context Panel"
    >
      {/* ── Top Header ── */}
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between pt-1 pb-2.5 border-b border-white/[0.08]">
          <div className="flex items-center gap-2">
            <div className="p-1 rounded-lg bg-violet-500/15 border border-violet-400/30 flex items-center justify-center">
              <Cpu className="w-3.5 h-3.5 text-violet-300" />
            </div>
            <span
              className="font-extrabold text-xs tracking-wider text-white uppercase font-mono"
              style={{ fontFamily: 'Orbitron, sans-serif' }}
            >
              INTELLIGENCE CONTEXT
            </span>
          </div>

          {onClose && (
            <button
              type="button"
              onClick={onClose}
              className="p-1 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] text-neutral-400 hover:text-white transition-colors cursor-pointer lg:hidden"
              title="Close Intelligence Panel"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* ── Tab Switcher ── */}
        <div className="grid grid-cols-3 bg-white/[0.03] border border-white/[0.08] p-1 rounded-xl font-mono text-[10px]">
          <button
            type="button"
            onClick={() => setActiveTab('telemetry')}
            className={`py-1.5 px-2 rounded-lg font-semibold transition-all duration-150 flex items-center justify-center gap-1 cursor-pointer ${
              activeTab === 'telemetry'
                ? 'bg-violet-500/20 text-white border border-violet-400/40 shadow-sm'
                : 'text-neutral-400 hover:text-neutral-200'
            }`}
          >
            <Activity className="w-3 h-3 text-cyan-400" />
            <span>STATUS</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('knowledge')}
            className={`py-1.5 px-2 rounded-lg font-semibold transition-all duration-150 flex items-center justify-center gap-1 cursor-pointer ${
              activeTab === 'knowledge'
                ? 'bg-violet-500/20 text-white border border-violet-400/40 shadow-sm'
                : 'text-neutral-400 hover:text-neutral-200'
            }`}
          >
            <Layers className="w-3 h-3 text-violet-400" />
            <span>CONTEXT</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('documents')}
            className={`py-1.5 px-2 rounded-lg font-semibold transition-all duration-150 flex items-center justify-center gap-1 cursor-pointer ${
              activeTab === 'documents'
                ? 'bg-violet-500/20 text-white border border-violet-400/40 shadow-sm'
                : 'text-neutral-400 hover:text-neutral-200'
            }`}
          >
            <Database className="w-3 h-3 text-emerald-400" />
            <span>RAG DOCS</span>
          </button>
        </div>
      </div>

      {/* ── Main Content Area ── */}
      <div className="flex-1 my-3 overflow-y-auto hud-scrollbar flex flex-col gap-3 pr-0.5">
        {/* ── Tab 1: Agent Status & Telemetry ── */}
        {activeTab === 'telemetry' && (
          <div className="flex flex-col gap-3">
            {/* System Status Card */}
            <div className="p-3 rounded-2xl bg-white/[0.02] border border-white/[0.08] flex flex-col gap-2.5">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold font-mono tracking-wider text-neutral-400 uppercase">
                  AGENT RUNTIME
                </span>
                <span className="flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-[10px] font-mono text-emerald-400 font-bold">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  ONLINE
                </span>
              </div>

              <div className="flex items-center justify-between pt-1 border-t border-white/[0.06]">
                <span className="text-[11px] text-neutral-400">Current Phase</span>
                <span className="text-xs font-mono font-bold text-cyan-300 tracking-wide uppercase">
                  {currentPhase}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-[11px] text-neutral-400">Session Ref</span>
                <span className="text-[10px] font-mono text-neutral-300 truncate max-w-[130px]">
                  {currentSessionId || 'default_session'}
                </span>
              </div>
            </div>

            {/* Live Reasoning Telemetry Card */}
            <div className="p-3 rounded-2xl bg-white/[0.02] border border-white/[0.08] flex flex-col gap-2.5">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold font-mono tracking-wider text-neutral-400 uppercase">
                  REASONING TELEMETRY
                </span>
                {agentLoading && <Loader2 className="w-3.5 h-3.5 text-violet-400 animate-spin" />}
              </div>

              {stepsCount > 0 ? (
                <div className="flex flex-col gap-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-neutral-400">Completed Steps</span>
                    <span className="font-mono text-violet-300 font-bold">{stepsCount}</span>
                  </div>

                  {lastStep && (
                    <div className="p-2.5 rounded-xl bg-neutral-900/80 border border-white/[0.06] flex flex-col gap-1">
                      <div className="text-[10px] font-mono text-cyan-400 font-semibold uppercase flex items-center gap-1">
                        <ChevronRight className="w-3 h-3 text-cyan-400" />
                        {lastStep.action || 'Thinking Step'}
                      </div>
                      <p className="text-[11px] text-neutral-300 leading-relaxed font-sans line-clamp-3">
                        {lastStep.thought || lastStep.output || 'Processing agent reasoning loop...'}
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="py-4 text-center text-neutral-500 font-mono text-xs flex flex-col items-center gap-1">
                  <Activity className="w-4 h-4 text-neutral-600 animate-pulse" />
                  <span>WAITING FOR EXECUTION</span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* ── Tab 2: Knowledge Context (RAG Chunks) ── */}
        {activeTab === 'knowledge' && (
          <div className="flex flex-col gap-3">
            <div className="p-3 rounded-2xl bg-white/[0.02] border border-white/[0.08] flex flex-col gap-2.5">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold font-mono tracking-wider text-neutral-400 uppercase">
                  RETRIEVED KNOWLEDGE
                </span>
                <span className="text-[10px] font-mono text-violet-300">
                  {retrievedContext.length} items
                </span>
              </div>

              {retrievedContext.length > 0 ? (
                <div className="flex flex-col gap-2 max-h-72 overflow-y-auto hud-scrollbar pr-1">
                  {retrievedContext.map((c, i) => (
                    <div
                      key={i}
                      className="p-2.5 rounded-xl bg-neutral-900/80 border border-white/[0.06] flex flex-col gap-1"
                    >
                      <div className="flex items-center justify-between text-[11px]">
                        <span className="font-semibold text-cyan-300 truncate max-w-[140px] flex items-center gap-1">
                          <FileText className="w-3 h-3 text-cyan-400" />
                          {c.filename || 'Document Chunk'}
                        </span>
                        {c.similarity && (
                          <span className="font-mono text-[10px] text-neutral-400">
                            {(c.similarity * 100).toFixed(0)}% match
                          </span>
                        )}
                      </div>
                      <p className="text-[11px] text-neutral-300 leading-relaxed font-sans line-clamp-3">
                        {c.text}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="py-6 text-center text-neutral-500 font-mono text-xs flex flex-col items-center gap-1.5">
                  <Layers className="w-5 h-5 text-neutral-600" />
                  <span>NO ACTIVE KNOWLEDGE CONTEXT</span>
                  <span className="text-[10px] text-neutral-600 font-sans">
                    Ask a question referencing uploaded documents
                  </span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* ── Tab 3: RAG Document Management ── */}
        {activeTab === 'documents' && (
          <div className="flex flex-col gap-3">
            {/* Document Uploader Header */}
            <div className="p-3 rounded-2xl bg-white/[0.02] border border-white/[0.08] flex flex-col gap-2.5">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold font-mono tracking-wider text-neutral-400 uppercase">
                  DOCUMENT KNOWLEDGE BASE
                </span>
                <label className="cursor-pointer px-2.5 py-1 rounded-xl bg-violet-500/20 hover:bg-violet-500/30 border border-violet-400/40 text-violet-200 text-[10px] font-mono font-bold uppercase tracking-wider flex items-center gap-1 transition-all">
                  {uploadingDoc ? (
                    <Loader2 className="w-3 h-3 animate-spin" />
                  ) : (
                    <Plus className="w-3 h-3" />
                  )}
                  <span>UPLOAD</span>
                  <input
                    type="file"
                    className="hidden"
                    accept=".txt,.pdf,.md,.csv,.json"
                    onChange={(e) => {
                      if (e.target.files?.[0] && onUploadDoc) {
                        onUploadDoc(e.target.files[0]);
                        e.target.value = '';
                      }
                    }}
                  />
                </label>
              </div>

              {documents.length > 0 ? (
                <div className="flex flex-col gap-2 max-h-64 overflow-y-auto hud-scrollbar pr-1">
                  {documents.map((doc) => (
                    <div
                      key={doc.id || doc.filename}
                      className="p-2.5 rounded-xl bg-neutral-900/80 border border-white/[0.06] flex items-center justify-between gap-2"
                    >
                      <div className="flex items-center gap-2 min-w-0">
                        <FileText className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                        <div className="flex flex-col min-w-0">
                          <span className="text-xs font-medium text-neutral-200 truncate">
                            {doc.filename || doc.name || 'Document'}
                          </span>
                          <span className="text-[9px] font-mono text-neutral-500">
                            {doc.chunks_count ? `${doc.chunks_count} chunks` : 'Indexed'}
                          </span>
                        </div>
                      </div>

                      {onDeleteDoc && (
                        <button
                          type="button"
                          onClick={() => onDeleteDoc(doc.id)}
                          className="p-1 text-neutral-500 hover:text-red-400 hover:bg-red-500/20 rounded-md transition-colors shrink-0"
                          title="Delete document"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="py-6 text-center text-neutral-500 font-mono text-xs flex flex-col items-center gap-1.5">
                  <Upload className="w-5 h-5 text-neutral-600" />
                  <span>NO DOCUMENTS UPLOADED</span>
                  <span className="text-[10px] text-neutral-600 font-sans">
                    Upload TXT, PDF, MD, CSV or JSON files for RAG
                  </span>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* ── Footer ── */}
      <div className="pt-2.5 border-t border-white/[0.08] flex items-center justify-between text-[10px] font-mono text-neutral-400">
        <div className="flex items-center gap-1.5">
          <Shield className="w-3 h-3 text-violet-400" />
          <span>DOXA SECURITY CORE</span>
        </div>
        <span className="text-emerald-400 font-semibold">ACTIVE</span>
      </div>
    </aside>
  );
}
