import { useState } from "react";
import { PipelineTabs, type StageTab } from "./components/Tabs";
import { RequirementInput } from "./components/RequirementInput";
import { RequirementAnalysis } from "./components/RequirementAnalysis";
import { TaskDecomposition } from "./components/TaskDecomposition";
import { EngineeringArtifacts } from "./components/EngineeringArtifacts";
import { ValidationReport } from "./components/ValidationReport";
import { RiskAnalysis } from "./components/RiskAnalysis";
import { FinalSummary } from "./components/FinalSummary";
import { UrlShortenerDemo } from "./components/UrlShortenerDemo";
import { analyzeRequirement } from "./api/client";
import type { CopilotResponse } from "./types";

const STAGES: StageTab[] = [
  { id: "analysis", label: "Requirement Analysis", index: 1 },
  { id: "tasks", label: "Task Decomposition", index: 2 },
  { id: "artifacts", label: "Engineering Artifacts", index: 3 },
  { id: "validation", label: "Validation", index: 4 },
  { id: "risks", label: "Risk Analysis", index: 5 },
  { id: "summary", label: "Final Summary", index: 6 },
  { id: "demo", label: "Live Demo", index: 7 },
];

function App() {
  const [result, setResult] = useState<CopilotResponse | null>(null);
  const [activeTab, setActiveTab] = useState<string>("demo");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleGenerate(requirement: string) {
    setLoading(true);
    setError(null);
    try {
      const data = await analyzeRequirement(requirement);
      setResult(data);
      setActiveTab("analysis");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Analysis failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-console-bg text-console-text">
      <header className="border-b border-console-border bg-console-panel/60 px-6 py-4">
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <div>
            <p className="font-mono text-[10px] uppercase tracking-[0.25em] text-console-accent">
              engineering copilot<span className="cursor-blink">_</span>
            </p>
            <h1 className="text-lg font-semibold text-console-text">
              AI-Assisted Software Engineering Console
            </h1>
          </div>
          <div className="hidden font-mono text-[10px] text-console-muted sm:block">
            engineer-led · AI-assisted · fully validated
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl space-y-5 px-6 py-6">
        <RequirementInput onSubmit={handleGenerate} loading={loading} />

        {error && (
          <p className="rounded border border-console-danger/40 bg-console-danger/10 px-4 py-3 font-mono text-xs text-console-danger">
            {error}
          </p>
        )}

        <div className="rounded-lg border border-console-border shadow-panel">
          <PipelineTabs stages={STAGES} activeId={activeTab} onSelect={setActiveTab} />
          <div className="bg-console-bg p-5">
            {activeTab === "demo" && <UrlShortenerDemo />}

            {activeTab !== "demo" && !result && (
              <p className="py-10 text-center font-mono text-sm text-console-muted">
                Enter a requirement above and click Generate to produce the engineering
                breakdown for this stage.
              </p>
            )}

            {activeTab === "analysis" && result && (
              <RequirementAnalysis data={result.requirement_analysis} />
            )}
            {activeTab === "tasks" && result && (
              <TaskDecomposition tasks={result.task_decomposition} />
            )}
            {activeTab === "artifacts" && result && (
              <EngineeringArtifacts data={result.engineering_artifacts} />
            )}
            {activeTab === "validation" && result && (
              <ValidationReport data={result.validation} />
            )}
            {activeTab === "risks" && result && <RiskAnalysis data={result.risk_analysis} />}
            {activeTab === "summary" && result && <FinalSummary data={result.final_summary} />}
          </div>
        </div>
      </main>

      <footer className="mx-auto max-w-6xl px-6 py-6 font-mono text-[10px] text-console-muted">
        AI assists the engineer within tasks; the engineer owns execution and quality.
      </footer>
    </div>
  );
}

export default App;
