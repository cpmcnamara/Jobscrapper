export type CategoryId =
  | "ai_strategy"
  | "data_readiness"
  | "ai_ml_engineering"
  | "domain_ai"
  | "genai_llm"
  | "uncategorized";

export type SeniorityLevel =
  | "intern"
  | "junior"
  | "mid"
  | "senior"
  | "lead"
  | "principal"
  | "director"
  | "vp"
  | "c_level"
  | "unknown";

export type Sector = "consulting" | "tech";

export interface Job {
  title: string;
  titleRaw: string;
  company: string;
  companySlug: string;
  sector: Sector;
  category: CategoryId;
  seniority: SeniorityLevel;
  city: string;
  state: string;
  country: string;
  isRemote: boolean;
  url: string;
  firstSeen: string;
  lastSeen: string;
}

export interface TrendPoint {
  date: string;
  total: number;
  byCategory: Record<string, number>;
  bySector: Record<string, number>;
  byCompany: Record<string, number>;
}

export interface CompanyData {
  slug: string;
  name: string;
  sector: Sector;
  totalActiveJobs: number;
  byCategory: Record<string, number>;
  bySeniority: Record<string, number>;
  topRoles: { title: string; count: number }[];
}

export interface CategoryData {
  id: string;
  name: string;
  totalJobs: number;
  byCompany: Record<string, number>;
  bySeniority: Record<string, number>;
  topTitles: { title: string; count: number }[];
}

export interface GeoLocation {
  country: string;
  state: string;
  city: string;
  isRemote: boolean;
  company: string;
  category: string;
  count: number;
}

export interface Overview {
  totalActiveJobs: number;
  totalCompanies: number;
  topCategory: string;
  topCategoryId: string;
  consultingVsTech: { consulting: number; tech: number };
  topGrowthCompany: string;
}

export interface FilterState {
  companies: string[];
  categories: CategoryId[];
  sectors: Sector[];
  search: string;
}
