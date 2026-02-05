"use client";

import { useEffect, useState } from "react";
import CompanyBarChart from "@/components/charts/CompanyBarChart";
import CategoryDonut from "@/components/charts/CategoryDonut";
import SeniorityStack from "@/components/charts/SeniorityStack";
import { fetchCompanies } from "@/lib/api";
import type { CompanyData, Sector } from "@/lib/types";

export default function CompaniesPage() {
  const [companies, setCompanies] = useState<CompanyData[]>([]);
  const [filter, setFilter] = useState<"all" | Sector>("all");
  const [selected, setSelected] = useState<CompanyData | null>(null);

  useEffect(() => {
    fetchCompanies().then((d) => setCompanies(d.companies)).catch(() => {});
  }, []);

  const filtered =
    filter === "all"
      ? companies
      : companies.filter((c) => c.sector === filter);

  const barData = filtered.map((c) => ({
    name: c.name,
    value: c.totalActiveJobs,
    sector: c.sector,
  }));

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-2">
        Company Comparison
      </h1>
      <p className="text-sm text-slate-500 mb-6">
        AI &amp; data job counts across tracked companies
      </p>

      <div className="flex gap-2 mb-6">
        {(["all", "consulting", "tech"] as const).map((s) => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === s
                ? "bg-slate-900 text-white"
                : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-100"
            }`}
          >
            {s === "all" ? "All" : s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
      </div>

      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm mb-6">
        <CompanyBarChart data={barData} />
      </div>

      <h2 className="text-lg font-semibold text-slate-800 mb-4">
        Company Details
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((c) => (
          <div
            key={c.slug}
            className={`bg-white rounded-xl border p-5 shadow-sm cursor-pointer transition-all ${
              selected?.slug === c.slug
                ? "border-blue-500 ring-2 ring-blue-100"
                : "border-slate-200 hover:border-slate-300"
            }`}
            onClick={() => setSelected(selected?.slug === c.slug ? null : c)}
          >
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-semibold text-slate-800">{c.name}</h3>
              <span
                className={`text-xs px-2 py-1 rounded-full ${
                  c.sector === "consulting"
                    ? "bg-purple-100 text-purple-700"
                    : "bg-blue-100 text-blue-700"
                }`}
              >
                {c.sector}
              </span>
            </div>
            <p className="text-2xl font-bold text-slate-800">
              {c.totalActiveJobs}
            </p>
            <p className="text-xs text-slate-400">active jobs</p>

            {selected?.slug === c.slug && (
              <div className="mt-4 pt-4 border-t border-slate-100">
                <p className="text-xs font-medium text-slate-500 mb-2">
                  Category breakdown
                </p>
                <CategoryDonut data={c.byCategory} />
                <p className="text-xs font-medium text-slate-500 mb-2 mt-4">
                  Seniority distribution
                </p>
                <SeniorityStack data={c.bySeniority} />
                {c.topRoles.length > 0 && (
                  <div className="mt-4">
                    <p className="text-xs font-medium text-slate-500 mb-2">
                      Top roles
                    </p>
                    <ul className="text-xs text-slate-600 space-y-1">
                      {c.topRoles.slice(0, 5).map((r, i) => (
                        <li key={i}>
                          {r.title}{" "}
                          <span className="text-slate-400">({r.count})</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
