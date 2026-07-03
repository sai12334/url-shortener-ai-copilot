import type {
  AnalyticsResponse,
  ApiError,
  CopilotResponse,
  ShortenResponse,
} from "../types";

const API_BASE =
  "https://url-shortener-ai-copilot-production.up.railway.app";

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let message = `Request failed with status ${res.status}`;
    try {
      const body: ApiError = await res.json();
      if (body.detail) message = body.detail;
    } catch {
      // response body wasn't JSON — keep the generic message
    }
    throw new Error(message);
  }
  return res.json() as Promise<T>;
}

export async function analyzeRequirement(
  requirement: string
): Promise<CopilotResponse> {
  const res = await fetch(`${API_BASE}/copilot/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ requirement }),
  });

  return handleResponse<CopilotResponse>(res);
}

export async function shortenUrl(
  originalUrl: string,
  customAlias?: string
): Promise<ShortenResponse> {
  const res = await fetch(`${API_BASE}/shorten`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      original_url: originalUrl,
      custom_alias: customAlias || undefined,
    }),
  });

  return handleResponse<ShortenResponse>(res);
}

export async function getAnalytics(
  shortCode: string
): Promise<AnalyticsResponse> {
  const res = await fetch(`${API_BASE}/analytics/${shortCode}`);

  return handleResponse<AnalyticsResponse>(res);
}
