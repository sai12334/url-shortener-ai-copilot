import { Panel } from "./Tabs";
import type { RiskAnalysis as RiskA } from "../types";

const CATEGORY_COLOR: Record<string, string> = {
  Functional: "text-console-info border-console-info/40",
  "AI-related": "text-console-warn border-console-warn/40",
  Design: "text-console-muted border-console-border",
  Scalability: "text-console-accent border-console-accent/40",
  Security: "text-console-danger border-console-danger/40",
};

export function RiskAnalysis({ data }: { data: RiskA }) {
  return (
    <Panel eyebrow="05 · Risk Analysis" title="Risks, categories, and mitigations">
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="border-b border-console-border text-left font-mono text-[10px] uppercase tracking-wide text-console-muted">
              <th className="py-2 pr-3">Category</th>
              <th className="py-2 pr-3">Risk</th>
              <th className="py-2">Mitigation</th>
            </tr>
          </thead>
          <tbody>
            {data.risks.map((r, i) => (
              <tr key={i} className="border-b border-console-border/60 align-top">
                <td className="py-3 pr-3">
                  <span
                    className={`rounded border px-1.5 py-0.5 font-mono text-[10px] ${
                      CATEGORY_COLOR[r.category] ?? "text-console-muted border-console-border"
                    }`}
                  >
                    {r.category}
                  </span>
                </td>
                <td className="py-3 pr-3 text-console-text/90">{r.risk}</td>
                <td className="py-3 text-console-text/70">{r.mitigation}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Panel>
  );
}
