import React, { useRef, useState } from "react";
import { motion } from "framer-motion";
import {
  Upload,
  Send,
  Loader2,
  CheckCircle2,
  AlertCircle,
  FileText,
  Sparkles,
  MessageSquare,
  ShieldCheck,
  Brain,
} from "lucide-react";

function Pill({ children }) {
  return (
    <span className="inline-flex items-center rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs font-medium text-white/80 backdrop-blur">
      {children}
    </span>
  );
}

function InfoCard({ icon: Icon, title, text }) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-4 backdrop-blur">
      <div className="mb-3 flex h-11 w-11 items-center justify-center rounded-2xl bg-white/10">
        <Icon className="h-5 w-5 text-white" />
      </div>
      <h3 className="text-sm font-semibold text-white">{title}</h3>
      <p className="mt-1 text-sm leading-6 text-white/65">{text}</p>
    </div>
  );
}

export default function ProjectIntelligenceUI() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [uploadError, setUploadError] = useState("");

  const [query, setQuery] = useState("");
  const [asking, setAsking] = useState(false);
  const [chatResult, setChatResult] = useState(null);
  const [chatError, setChatError] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  const fileInputRef = useRef(null);
 const apiBase =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8001";

  const handleFilePick = (event) => {
    const file = event.target.files?.[0] || null;
    setSelectedFile(file);
    setUploadError("");
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files?.[0] || null;
    if (file) {
      setSelectedFile(file);
      setUploadError("");
    }
  };

  const uploadFile = async () => {
    if (!selectedFile) {
      setUploadError("Choose a file first.");
      return;
    }

    setUploading(true);
    setUploadError("");
    setUploadResult(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${apiBase}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Upload failed.");
      }

      setUploadResult(data);
    } catch (error) {
      setUploadError(error.message || "Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  const askQuestion = async () => {
    const finalQuery = query.trim();
    if (!finalQuery) {
      setChatError("Type a question first.");
      return;
    }

    setAsking(true);
    setChatError("");

    try {
      const response = await fetch(`${apiBase}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: finalQuery,
          session_id: "default",
        }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Chat request failed.");
      }

      setChatResult(data);
      setChatHistory((prev) => [
        {
          id: Date.now(),
          query: finalQuery,
          answer: data.answer,
          confidence: data.confidence,
          agent: data.agent_used,
          sources: data.sources || [],
        },
        ...prev,
      ]);
    } catch (error) {
      setChatError(error.message || "Chat request failed.");
    } finally {
      setAsking(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#060816] text-white">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute left-1/2 top-[-120px] h-[360px] w-[360px] -translate-x-1/2 rounded-full bg-cyan-500/20 blur-3xl" />
        <div className="absolute right-[-80px] top-[160px] h-[280px] w-[280px] rounded-full bg-fuchsia-500/15 blur-3xl" />
        <div className="absolute bottom-[-80px] left-[-40px] h-[260px] w-[260px] rounded-full bg-blue-500/15 blur-3xl" />
      </div>

      <div className="relative mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="mb-8 rounded-[32px] border border-white/10 bg-white/5 p-6 shadow-2xl shadow-black/30 backdrop-blur-xl"
        >
          <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
            <div>
              <div className="mb-4 flex flex-wrap gap-2">
                <Pill>Modern React UI</Pill>
                <Pill>FastAPI Connected</Pill>
                <Pill>Upload + Chat</Pill>
              </div>

              <h1 className="max-w-3xl text-4xl font-bold tracking-tight text-white sm:text-5xl">
                Upload documents and chat with them in one clean workspace.
              </h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-white/70">
                This system lets you upload project files, index them through your backend,
                and ask natural language questions for quick summaries, risks, progress, and key details.
              </p>
            </div>

            <div className="grid gap-4 sm:grid-cols-3 lg:grid-cols-1">
              <InfoCard
                icon={ShieldCheck}
                title="Document indexing"
                text="Upload PDF, CSV, TXT, or DOCX files and store them for retrieval."
              />
              <InfoCard
                icon={Brain}
                title="AI-powered answers"
                text="Ask questions and get summarized responses from the indexed document context."
              />
              <InfoCard
                icon={MessageSquare}
                title="Fast workflow"
                text="Simple upload and chat flow without extra settings or clutter on the screen."
              />
            </div>
          </div>
        </motion.div>

        <div className="grid gap-6 lg:grid-cols-2">
          <motion.div
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05, duration: 0.35 }}
            className="rounded-[32px] border border-white/10 bg-white/5 p-6 shadow-2xl shadow-black/20 backdrop-blur-xl"
          >
            <div className="mb-5 flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-500/15">
                <Upload className="h-5 w-5 text-cyan-300" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-white">Upload file</h2>
                <p className="text-sm text-white/60">Send a document to your backend for indexing</p>
              </div>
            </div>

            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
              className="rounded-[28px] border border-dashed border-white/15 bg-black/20 p-6 text-center"
            >
              <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-3xl bg-white/10">
                <FileText className="h-8 w-8 text-white/90" />
              </div>

              <h3 className="text-lg font-semibold text-white">Drop your file here</h3>
              <p className="mt-2 text-sm text-white/60">PDF, CSV, TXT, DOCX</p>

              <input
                ref={fileInputRef}
                type="file"
                onChange={handleFilePick}
                accept=".pdf,.csv,.txt,.docx"
                className="hidden"
              />

              <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:justify-center">
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="rounded-2xl bg-white px-5 py-3 text-sm font-semibold text-slate-900 transition hover:opacity-90"
                >
                  Choose file
                </button>
                <button
                  onClick={uploadFile}
                  disabled={uploading}
                  className="inline-flex items-center justify-center gap-2 rounded-2xl border border-white/15 bg-white/10 px-5 py-3 text-sm font-semibold text-white transition hover:bg-white/15 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {uploading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Upload className="h-4 w-4" />}
                  {uploading ? "Uploading" : "Upload now"}
                </button>
              </div>

              {selectedFile && (
                <div className="mt-5 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-left">
                  <p className="truncate text-sm font-medium text-white">{selectedFile.name}</p>
                  <p className="mt-1 text-xs text-white/50">{(selectedFile.size / 1024).toFixed(1)} KB</p>
                </div>
              )}
            </div>

            {uploadError && (
              <div className="mt-4 flex items-start gap-3 rounded-2xl border border-rose-500/30 bg-rose-500/10 p-4 text-sm text-rose-200">
                <AlertCircle className="mt-0.5 h-4 w-4" />
                <span>{uploadError}</span>
              </div>
            )}

            {uploadResult && (
              <div className="mt-4 rounded-2xl border border-emerald-500/25 bg-emerald-500/10 p-4">
                <div className="mb-3 flex items-center gap-2 text-emerald-200">
                  <CheckCircle2 className="h-4 w-4" />
                  <span className="text-sm font-semibold">Upload successful</span>
                </div>

                <div className="grid gap-3 sm:grid-cols-3">
                  <div className="rounded-2xl bg-black/20 p-3">
                    <p className="text-xs text-white/45">Filename</p>
                    <p className="mt-1 truncate text-sm font-medium text-white">{uploadResult.filename}</p>
                  </div>
                  <div className="rounded-2xl bg-black/20 p-3">
                    <p className="text-xs text-white/45">Chunks stored</p>
                    <p className="mt-1 text-sm font-medium text-white">{uploadResult.chunks_stored}</p>
                  </div>
                  <div className="rounded-2xl bg-black/20 p-3">
                    <p className="text-xs text-white/45">Document ID</p>
                    <p className="mt-1 truncate text-sm font-medium text-white">{uploadResult.doc_id}</p>
                  </div>
                </div>
              </div>
            )}
          </motion.div>

          <div className="space-y-6">
            <motion.div
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1, duration: 0.35 }}
              className="rounded-[32px] border border-white/10 bg-white/5 p-6 shadow-2xl shadow-black/20 backdrop-blur-xl"
            >
              <div className="mb-5 flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-fuchsia-500/15">
                  <MessageSquare className="h-5 w-5 text-fuchsia-300" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-white">Chat with document</h2>
                  <p className="text-sm text-white/60">Ask questions based on uploaded content</p>
                </div>
              </div>

              <div className="space-y-4">
                <textarea
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  rows={6}
                  placeholder="Ask something like: summarize the file, list the risks, or show the deadlines..."
                  className="w-full rounded-[24px] border border-white/10 bg-black/20 px-4 py-4 text-sm leading-6 text-white outline-none transition placeholder:text-white/35 focus:border-cyan-400/50"
                />

                <button
                  onClick={askQuestion}
                  disabled={asking}
                  className="inline-flex w-full items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-cyan-400 to-blue-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:opacity-95 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {asking ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                  {asking ? "Generating answer" : "Send question"}
                </button>

                {chatError && (
                  <div className="flex items-start gap-3 rounded-2xl border border-rose-500/30 bg-rose-500/10 p-4 text-sm text-rose-200">
                    <AlertCircle className="mt-0.5 h-4 w-4" />
                    <span>{chatError}</span>
                  </div>
                )}

                <div className="rounded-[24px] border border-white/10 bg-black/20 p-4">
                  {!chatResult ? (
                    <div className="py-12 text-center">
                      <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-white/10">
                        <Sparkles className="h-6 w-6 text-white/80" />
                      </div>
                      <p className="text-sm font-medium text-white">No answer yet</p>
                      <p className="mt-1 text-sm text-white/50">Upload a file and ask your first question.</p>
                    </div>
                  ) : (
                    <div>
                      <div className="mb-3 flex flex-wrap gap-2">
                        <Pill>{chatResult.agent_used || "agent"}</Pill>
                        <Pill>{chatResult.confidence || "unknown"}</Pill>
                      </div>

                      <p className="whitespace-pre-wrap text-sm leading-7 text-white/80">
                        {chatResult.answer}
                      </p>

                      {chatResult.sources?.length > 0 && (
                        <div className="mt-4 border-t border-white/10 pt-4">
                          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-white/45">Sources</p>
                          <div className="flex flex-wrap gap-2">
                            {chatResult.sources.map((source) => (
                              <Pill key={source}>{source}</Pill>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15, duration: 0.35 }}
              className="rounded-[32px] border border-white/10 bg-white/5 p-6 shadow-2xl shadow-black/20 backdrop-blur-xl"
            >
              <div className="mb-5 flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-white/10">
                  <MessageSquare className="h-5 w-5 text-white/80" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-white">Chat history</h2>
                  <p className="text-sm text-white/60">Recent questions and answers in this session</p>
                </div>
              </div>

              {chatHistory.length === 0 ? (
                <div className="rounded-[24px] border border-white/10 bg-black/20 px-4 py-10 text-center">
                  <p className="text-sm font-medium text-white">No history yet</p>
                  <p className="mt-1 text-sm text-white/50">Your recent chat messages will appear here.</p>
                </div>
              ) : (
                <div className="space-y-4 max-h-[520px] overflow-auto pr-1">
                  {chatHistory.map((item) => (
                    <div key={item.id} className="rounded-[24px] border border-white/10 bg-black/20 p-4">
                      <div className="mb-3 flex flex-wrap gap-2">
                        <Pill>{item.agent || "agent"}</Pill>
                        <Pill>{item.confidence || "unknown"}</Pill>
                      </div>
                      <p className="text-sm font-semibold text-white">{item.query}</p>
                      <p className="mt-3 whitespace-pre-wrap text-sm leading-7 text-white/75 line-clamp-6">
                        {item.answer}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
