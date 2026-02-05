export const CATEGORY_LABELS: Record<string, string> = {
  ai_strategy: "AI / Data Strategy",
  data_readiness: "Data Readiness / Engineering",
  ai_ml_engineering: "AI / ML Engineering",
  domain_ai: "Business Context / Domain AI",
  genai_llm: "Gen AI / LLM",
  uncategorized: "Other",
};

export const CATEGORY_COLORS: Record<string, string> = {
  ai_strategy: "#6366f1",
  data_readiness: "#06b6d4",
  ai_ml_engineering: "#f59e0b",
  domain_ai: "#10b981",
  genai_llm: "#ef4444",
  uncategorized: "#94a3b8",
};

export const SECTOR_COLORS: Record<string, string> = {
  consulting: "#8b5cf6",
  tech: "#3b82f6",
};

export const SENIORITY_ORDER = [
  "intern", "junior", "mid", "senior", "lead",
  "principal", "director", "vp", "c_level",
];

export const SENIORITY_LABELS: Record<string, string> = {
  intern: "Intern",
  junior: "Junior",
  mid: "Mid-level",
  senior: "Senior",
  lead: "Lead",
  principal: "Principal",
  director: "Director",
  vp: "VP",
  c_level: "C-Level",
  unknown: "Unknown",
};
