import { Panel } from "./Tabs";
import type { FinalSummary as FS } from "../types";

export function FinalSummary({ data }: { data: FS }) {
  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
      <Panel eyebrow="06 · Summary" title="Implementation approach">
        <p className="text-sm leading-relaxed text-console-text/90">{data.implementation_approach}</p>
      </Panel>
      <Panel eyebrow="06 · Summary" title="Generated artifacts">
        <ul className="space-y-1.5">
          {data.generated_artifacts.map((a, i) => (
            <li key={i} className="flex gap-2 text-sm text-console-text/90">
              <span className="text-console-accent">✓</span>
              <span>{a}</span>
            </li>
          ))}
        </ul>
      </Panel>
      <Panel eyebrow="06 · Summary" title="Risks & validation">
        <p className="text-sm leading-relaxed text-console-text/90">{data.risks_and_validation}</p>
      </Panel>
      <Panel eyebrow="06 · Summary" title="Assumptions & limitations">
        <p className="text-sm leading-relaxed text-console-text/90">{data.assumptions_and_limitations}</p>
      </Panel>
    </div>
  );
}
