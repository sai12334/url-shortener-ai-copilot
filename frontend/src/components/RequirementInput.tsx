import { useState } from "react";

interface Props {
  onSubmit: (requirement: string) => void;
  loading: boolean;
}

const EXAMPLES = [
  {
    label: "Mandatory use case",
    text: "Build a scalable URL shortener service with APIs, persistence, and analytics.",
  },
  {
    label: "Brownfield",
    text: "Add rate limiting to the existing /shorten endpoint to prevent abuse.",
  },
  {
    label: "Ambiguous",
    text: "Make the link service more robust and user-friendly.",
  },
];

export function RequirementInput({ onSubmit, loading }: Props) {
  const [value, setValue] = useState(
    "Build a scalable URL shortener service with APIs, persistence, and analytics."
  );

  return (
    <div className="rounded-lg border border-console-border bg-console-panel p-5 shadow-panel">
      <div className="mb-3 flex items-baseline justify-between">
        <label className="font-mono text-[10px] uppercase tracking-[0.2em] text-console-accent">
          requirement.input
        </label>
        <span className="font-mono text-[10px] text-console-muted">
          {value.length} chars
        </span>
      </div>
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        rows={4}
        placeholder="Describe a software requirement — e.g. 'Build a scalable URL shortener service with APIs, persistence, and analytics.'"
        className="w-full resize-none rounded-md border border-console-border bg-console-bg px-3 py-2 font-mono text-sm text-console-text placeholder:text-console-muted focus:border-console-accent focus:outline-none"
      />
      <div className="mt-3 flex flex-wrap items-center gap-2">
        {EXAMPLES.map((ex) => (
          <button
            key={ex.label}
            onClick={() => setValue(ex.text)}
            className="rounded border border-console-border px-2.5 py-1 font-mono text-[11px] text-console-muted transition-colors hover:border-console-accent hover:text-console-accent"
          >
            {ex.label}
          </button>
        ))}
        <div className="flex-1" />
        <button
          onClick={() => onSubmit(value)}
          disabled={loading || value.trim().length < 10}
          className="rounded-md bg-console-accent px-4 py-2 font-mono text-xs font-semibold text-console-bg transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {loading ? "Analyzing…" : "Generate ▸"}
        </button>
      </div>
    </div>
  );
}
