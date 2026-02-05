"use client";

import { useEffect, useState } from "react";
import DataTable from "@/components/data/DataTable";
import ExportButton from "@/components/data/ExportButton";
import { fetchJobs } from "@/lib/api";
import type { Job } from "@/lib/types";

export default function JobsPage() {
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    fetchJobs().then((d) => setJobs(d.jobs)).catch(() => {});
  }, []);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">All Jobs</h1>
          <p className="text-sm text-slate-500 mt-1">
            Browse and search all tracked positions
          </p>
        </div>
        <ExportButton jobs={jobs} />
      </div>

      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
        <DataTable jobs={jobs} />
      </div>
    </div>
  );
}
