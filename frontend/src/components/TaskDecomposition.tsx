import { Panel } from "./Tabs";
import type { EngineeringTask } from "../types";

export function TaskDecomposition({ tasks }: { tasks: EngineeringTask[] }) {
  return (
    <Panel eyebrow="02 · Task Decomposition" title="Engineer-led execution sequence">
      <ol className="space-y-4">
        {tasks.map((task) => (
          <li key={task.id} className="rounded-md border border-console-border bg-console-panelAlt p-4">
            <div className="flex flex-wrap items-center gap-2">
              <span className="font-mono text-xs font-semibold text-console-accent">{task.id}</span>
              <h3 className="text-sm font-semibold text-console-text">{task.title}</h3>
              {task.depends_on.length > 0 && (
                <span className="ml-auto flex gap-1 font-mono text-[10px] text-console-muted">
                  depends on
                  {task.depends_on.map((d) => (
                    <span key={d} className="rounded border border-console-border px-1.5 py-0.5">
                      {d}
                    </span>
                  ))}
                </span>
              )}
            </div>
            <p className="mt-2 text-sm text-console-text/80">{task.description}</p>
            <div className="mt-3 rounded border border-console-accentDim/60 bg-console-accent/5 px-3 py-2">
              <p className="font-mono text-[10px] uppercase tracking-wide text-console-accent">AI assistance</p>
              <p className="mt-1 text-xs text-console-text/80">{task.ai_assistance}</p>
            </div>
          </li>
        ))}
      </ol>
    </Panel>
  );
}
