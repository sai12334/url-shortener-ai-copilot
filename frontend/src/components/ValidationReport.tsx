import { Panel } from "./Tabs";
import type { ValidationFinding, ValidationReport as VR } from "../types";

function severityColor(severity: string): string {
  const s = severity.toLowerCase();
  if (s.includes("open")) return "text-console-danger border-console-danger/40 bg-console-danger/10";
  if (s.includes("fixed") || s.includes("verified")) return "text-console-accent border-console-accent/40 bg-console-accent/10";
  return "text-console-muted border-console-border";
}

function FindingList({ items }: { items: ValidationFinding[] }) {
  return (
    <ul className="space-y-2">
      {items.map((f, i) => (
        <li key={i} className="rounded border border-console-border bg-console-panelAlt p-3 text-sm">
          <div className="flex items-center justify-between gap-2">
            <span className="font-mono text-xs text-console-info">{f.area}</span>
            <span className={`rounded border px-1.5 py-0.5 font-mono text-[10px] ${severityColor(f.severity)}`}>
              {f.severity}
            </span>
          </div>
          <p className="mt-1 text-console-text/80">{f.finding}</p>
        </li>
      ))}
    </ul>
  );
}

export function ValidationReport({ data }: { data: VR }) {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Panel eyebrow="04 · Validation" title="Code review">
          <FindingList items={data.code_review} />
        </Panel>
        <Panel eyebrow="04 · Validation" title="Security review">
          <FindingList items={data.security_review} />
        </Panel>
        <Panel eyebrow="04 · Validation" title="Performance review">
          <FindingList items={data.performance_review} />
        </Panel>
      </div>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Panel eyebrow="04 · Validation" title="Missing edge cases">
          <ul className="space-y-2">
            {data.missing_edge_cases.map((e, i) => (
              <li key={i} className="flex gap-2 text-sm text-console-text/90">
                <span className="text-console-warn">◆</span>
                <span>{e}</span>
              </li>
            ))}
          </ul>
        </Panel>
        <Panel eyebrow="04 · Validation" title="Test coverage summary">
          <p className="text-sm leading-relaxed text-console-text/90">{data.test_coverage_summary}</p>
        </Panel>
      </div>
    </div>
  );
}
