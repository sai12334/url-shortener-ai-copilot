import type { ReactNode } from "react";

export interface StageTab {
  id: string;
  label: string;
  index: number;
}

interface TabsProps {
  stages: StageTab[];
  activeId: string;
  onSelect: (id: string) => void;
}

export function PipelineTabs({ stages, activeId, onSelect }: TabsProps) {
  return (
    <div className="flex items-stretch overflow-x-auto border-b border-console-border bg-console-panel">
      {stages.map((stage, i) => {
        const isActive = stage.id === activeId;
        const isPast = stages.findIndex((s) => s.id === activeId) > i;
        return (
          <button
            key={stage.id}
            onClick={() => onSelect(stage.id)}
            className={`group relative flex items-center gap-2 whitespace-nowrap px-4 py-3 font-mono text-xs transition-colors ${
              isActive
                ? "text-console-accent"
                : isPast
                ? "text-console-text/70 hover:text-console-text"
                : "text-console-muted hover:text-console-text"
            }`}
          >
            <span
              className={`flex h-5 w-5 items-center justify-center rounded-full border text-[10px] ${
                isActive
                  ? "border-console-accent bg-console-accent/10 text-console-accent"
                  : isPast
                  ? "border-console-text/40 text-console-text/70"
                  : "border-console-muted/40 text-console-muted"
              }`}
            >
              {stage.index}
            </span>
            <span className="tracking-wide">{stage.label}</span>
            {isActive && (
              <span className="absolute inset-x-0 -bottom-px h-0.5 bg-console-accent" />
            )}
            {i < stages.length - 1 && (
              <span className="ml-2 text-console-border">→</span>
            )}
          </button>
        );
      })}
    </div>
  );
}

export function Panel({ children, title, eyebrow }: { children: ReactNode; title: string; eyebrow: string }) {
  return (
    <div className="rounded-lg border border-console-border bg-console-panel shadow-panel">
      <div className="border-b border-console-border px-5 py-3">
        <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-console-accent">{eyebrow}</p>
        <h2 className="mt-0.5 text-sm font-semibold text-console-text">{title}</h2>
      </div>
      <div className="p-5">{children}</div>
    </div>
  );
}
