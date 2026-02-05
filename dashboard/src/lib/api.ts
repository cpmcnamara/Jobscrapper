import type {
  Overview,
  TrendPoint,
  CompanyData,
  CategoryData,
  GeoLocation,
  Job,
} from "./types";

const BASE = "/data";

async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}/${path}`);
  if (!res.ok) throw new Error(`Failed to fetch ${path}`);
  return res.json();
}

export async function fetchOverview(): Promise<Overview> {
  return fetchJSON<Overview>("overview.json");
}

export async function fetchTrends(): Promise<{ timeSeries: TrendPoint[] }> {
  return fetchJSON("trends.json");
}

export async function fetchCompanies(): Promise<{ companies: CompanyData[] }> {
  return fetchJSON("companies.json");
}

export async function fetchCategories(): Promise<{ categories: CategoryData[] }> {
  return fetchJSON("categories.json");
}

export async function fetchGeo(): Promise<{
  locations: GeoLocation[];
  remoteTotal: number;
  topCountries: { country: string; count: number }[];
}> {
  return fetchJSON("geo.json");
}

export async function fetchJobs(): Promise<{ jobs: Job[] }> {
  return fetchJSON("jobs.json");
}

export async function fetchMetadata(): Promise<{
  lastUpdated: string;
  version: string;
}> {
  return fetchJSON("metadata.json");
}
