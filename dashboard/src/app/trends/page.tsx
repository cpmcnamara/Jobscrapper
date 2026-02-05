"use client";

import { useEffect, useState } from "react";
import TrendLineChart from "@/components/charts/TrendLineChart";
import { fetchTrends } from "@/lib/api";
import type { TrendPoint } from "@/lib/types";

export default function TrendsPage() {
  const [data, setData] = useState<TrendPoint[]>([]);
  const [mode, setMode] = useState<"total" | "byCategory" | "bySector">("total");

  useEffect(() => {
    fetchTrends().then((d) => setData(d.timeSeries)).catch(() => {});
  }, []);

  const modes: { key: typeof mode; label: string }[] = [
    { key: "total", label: "Total" },
    { key: "byCategory", label: "By Category" },
    { key: "bySector", label: "Consulting vs Tech" },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-2">Trends Over Time</h1>
      <p className="text-sm text-slate-500 mb-6">
        Job posting volume tracked across scrape runs
      </p>

      <div className="flex gap-2 mb-6">
        {modes.map((m) => (
          <button
            key={m.key}
            onClick={() => setMode(m.key)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              mode === m.key
                ? "bg-slate-900 text-white"
                : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-100"
            }`}
          >
            {m.label}
          </button>
        ))}
      </div>

      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
        {data.length > 0 ? (
          <TrendLineChart data={data} mode={mode} />
        ) : (
          <p className="text-slate-400 text-center py-12">
            Not enough data yet. Run the scraper multiple times to build trend data.
          </p>
        )}
      </div>
    </div>
  );
}
