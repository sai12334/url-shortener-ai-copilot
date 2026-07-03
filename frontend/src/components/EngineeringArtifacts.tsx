import { Panel } from "./Tabs";
import type { EngineeringArtifacts as EA } from "../types";

export function EngineeringArtifacts({ data }: { data: EA }) {
  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
      <Panel eyebrow="03 · Artifacts" title="Folder structure">
        <pre className="overflow-x-auto rounded bg-console-bg p-3 font-mono text-xs text-console-text/90">
{data.folder_structure.join("\n")}
        </pre>
      </Panel>

      <Panel eyebrow="03 · Artifacts" title="Database schema">
        <p className="font-mono text-xs leading-relaxed text-console-text/90">{data.database_schema}</p>
      </Panel>

      <Panel eyebrow="03 · Artifacts" title="API contracts">
        <ul className="space-y-2">
          {data.api_contracts.map((c, i) => (
            <li key={i} className="rounded bg-console-bg px-3 py-2 font-mono text-xs text-console-accent">
              {c}
            </li>
          ))}
        </ul>
      </Panel>

      <Panel eyebrow="03 · Artifacts" title="Key files">
        <ul className="space-y-2">
          {data.key_files.length === 0 && (
            <li className="text-sm text-console-muted">No key files generated for this requirement.</li>
          )}
          {data.key_files.map((f, i) => (
            <li key={i} className="text-sm">
              <span className="font-mono text-xs text-console-info">{f.path}</span>
              <p className="text-console-text/70">{f.description}</p>
            </li>
          ))}
        </ul>
      </Panel>
    </div>
  );
}
