import { useState } from "react";
import { Panel } from "./Tabs";
import { getAnalytics, shortenUrl } from "../api/client";
import type { AnalyticsResponse, ShortenResponse } from "../types";

interface LinkRow {
  data: ShortenResponse;
  analytics: AnalyticsResponse | null;
}

export function UrlShortenerDemo() {
  const [url, setUrl] = useState("");
  const [alias, setAlias] = useState("");
  const [links, setLinks] = useState<LinkRow[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleShorten() {
    setError(null);
    setSubmitting(true);
    try {
      const result = await shortenUrl(url.trim(), alias.trim() || undefined);
      setLinks((prev) => [{ data: result, analytics: null }, ...prev]);
      setUrl("");
      setAlias("");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to shorten URL");
    } finally {
      setSubmitting(false);
    }
  }

  async function refreshAnalytics(shortCode: string) {
    try {
      const data = await getAnalytics(shortCode);
      setLinks((prev) =>
        prev.map((l) => (l.data.short_code === shortCode ? { ...l, analytics: data } : l))
      );
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to fetch analytics");
    }
  }

  return (
    <Panel eyebrow="Live Demo" title="Mandatory use case — URL shortener (runs against the real API)">
      <div className="flex flex-col gap-3 sm:flex-row">
        <input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com/a/long/path"
          className="flex-1 rounded-md border border-console-border bg-console-bg px-3 py-2 font-mono text-sm text-console-text placeholder:text-console-muted focus:border-console-accent focus:outline-none"
        />
        <input
          value={alias}
          onChange={(e) => setAlias(e.target.value)}
          placeholder="custom alias (optional)"
          className="w-full rounded-md border border-console-border bg-console-bg px-3 py-2 font-mono text-sm text-console-text placeholder:text-console-muted focus:border-console-accent focus:outline-none sm:w-52"
        />
        <button
          onClick={handleShorten}
          disabled={submitting || url.trim().length === 0}
          className="rounded-md bg-console-accent px-4 py-2 font-mono text-xs font-semibold text-console-bg transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {submitting ? "Shortening…" : "Shorten"}
        </button>
      </div>

      {error && (
        <p className="mt-3 rounded border border-console-danger/40 bg-console-danger/10 px-3 py-2 font-mono text-xs text-console-danger">
          {error}
        </p>
      )}

      {links.length > 0 && (
        <div className="mt-5 overflow-x-auto">
          <table className="w-full border-collapse text-sm">
            <thead>
              <tr className="border-b border-console-border text-left font-mono text-[10px] uppercase tracking-wide text-console-muted">
                <th className="py-2 pr-3">Short URL</th>
                <th className="py-2 pr-3">Original</th>
                <th className="py-2 pr-3">Clicks</th>
                <th className="py-2">Last click</th>
              </tr>
            </thead>
            <tbody>
              {links.map((l) => (
                <tr key={l.data.short_code} className="border-b border-console-border/60">
                  <td className="py-2 pr-3">
                    <a
                      href={l.data.short_url}
                      target="_blank"
                      rel="noreferrer"
                      onClick={() => setTimeout(() => refreshAnalytics(l.data.short_code), 400)}
                      className="font-mono text-console-accent hover:underline"
                    >
                      {l.data.short_url}
                    </a>
                  </td>
                  <td className="max-w-xs truncate py-2 pr-3 text-console-text/70">
                    {l.data.original_url}
                  </td>
                  <td className="py-2 pr-3 font-mono text-console-text/90">
                    {l.analytics ? l.analytics.click_count : "—"}
                  </td>
                  <td className="py-2 text-console-text/70">
                    <div className="flex items-center gap-2">
                      <span>
                        {l.analytics?.last_clicked_at
                          ? new Date(l.analytics.last_clicked_at).toLocaleTimeString()
                          : "never"}
                      </span>
                      <button
                        onClick={() => refreshAnalytics(l.data.short_code)}
                        className="rounded border border-console-border px-1.5 py-0.5 font-mono text-[10px] text-console-muted hover:border-console-accent hover:text-console-accent"
                      >
                        refresh
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {links.length === 0 && !error && (
        <p className="mt-4 font-mono text-xs text-console-muted">
          No links yet — shorten a URL above, click it to trigger a redirect, then refresh analytics.
        </p>
      )}
    </Panel>
  );
}
