"use client";

import { useEffect, useState } from "react";
import StatCard from "@/components/data/StatCard";
import CategoryDonut from "@/components/charts/CategoryDonut";
import CompanyBarChart from "@/components/charts/CompanyBarChart";
import { fetchOverview, fetchCompanies, fetchJobs } from "@/lib/api";
import type { Overview, CompanyData, Job } from "@/lib/types";
import ExportButton from "@/components/data/ExportButton";

export default function HomePage() {
  const [overview, setOverview] = useState<Overview | null>(null);
  const [companies, setCompanies] = useState<CompanyData[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([fetchOverview(), fetchCompanies(), fetchJobs()])
      .then(([o, c, j]) => {
        setOverview(o);
        setCompanies(c.companies);
        setJobs(j.jobs);
      })
      .catch(() => setError("No data yet. Run the scraper first."));
  }, []);

  if (error) {
    return (
      <div className="max-w-2xl mx-auto mt-20 text-center">
        <h2 className="text-2xl font-bold text-slate-800 mb-4">
          No Data Available
        </h2>
        <p className="text-slate-500 mb-4">{error}</p>
        <code className="bg-slate-900 text-green-400 px-4 py-2 rounded text-sm">
          python -m backend.main
        </code>
      </div>
    );
  }

  if (!overview) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-slate-400">Loading...</p>
      </div>
    );
  }

  const catCounts: Record<string, number> = {};
  jobs.forEach((j) => {
    catCounts[j.category] = (catCounts[j.category] || 0) + 1;
  });

  const companyBars = companies.map((c) => ({
    name: c.name,
    value: c.totalActiveJobs,
    sector: c.sector,
  }));

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">
            AI Job Market Overview
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Tracking AI &amp; data roles across consulting and tech
          </p>
        </div>
        <ExportButton jobs={jobs} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          label="Total Active Jobs"
          value={overview.totalActiveJobs}
          color="#3b82f6"
        />
        <StatCard
          label="Companies Tracked"
          value={overview.totalCompanies}
        />
        <StatCard
          label="Consulting Jobs"
          value={overview.consultingVsTech.consulting}
          color="#8b5cf6"
        />
        <StatCard
          label="Tech Jobs"
          value={overview.consultingVsTech.tech}
          color="#3b82f6"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">
            Jobs by Category
          </h2>
          <CategoryDonut data={catCounts} />
        </div>
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">
            Jobs by Company
          </h2>
          <CompanyBarChart data={companyBars} />
        </div>
      </div>
    </div>
  );
}
