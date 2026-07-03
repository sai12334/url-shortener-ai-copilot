import { Panel } from "./Tabs";
import type { RequirementAnalysis as RA } from "../types";

export function RequirementAnalysis({ data }: { data: RA }) {
  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
      <Panel eyebrow="01 · Analysis" title="Functional requirements">
        <ul className="space-y-2">
          {data.functional_requirements.map((fr) => (
            <li key={fr.id} className="flex gap-3 text-sm">
              <span className="mt-0.5 shrink-0 font-mono text-xs text-console-accent">{fr.id}</span>
              <span className="text-console-text/90">{fr.description}</span>
            </li>
          ))}
        </ul>
      </Panel>

      <Panel eyebrow="01 · Analysis" title="Non-functional requirements">
        <ul className="space-y-3">
          {data.non_functional_requirements.map((nfr, i) => (
            <li key={i} className="text-sm">
              <span className="rounded bg-console-info/10 px-1.5 py-0.5 font-mono text-[10px] uppercase text-console-info">
                {nfr.category}
              </span>
              <p className="mt-1 text-console-text/90">{nfr.description}</p>
            </li>
          ))}
        </ul>
      </Panel>

      <Panel eyebrow="Flagged" title="Ambiguities">
        <ul className="space-y-2">
          {data.ambiguities.map((a, i) => (
            <li key={i} className="flex gap-2 text-sm text-console-text/90">
              <span className="mt-0.5 text-console-warn">▲</span>
              <span>{a}</span>
            </li>
          ))}
        </ul>
      </Panel>

      <Panel eyebrow="Stated" title="Assumptions">
        <ul className="space-y-2">
          {data.assumptions.map((a, i) => (
            <li key={i} className="flex gap-2 text-sm text-console-text/90">
              <span className="mt-0.5 text-console-accent">●</span>
              <span>{a}</span>
            </li>
          ))}
        </ul>
      </Panel>
    </div>
  );
}
