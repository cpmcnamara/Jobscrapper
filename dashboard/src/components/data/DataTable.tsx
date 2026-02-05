"use client";

import { useState, useMemo } from "react";
import type { Job } from "@/lib/types";
import { CATEGORY_LABELS, SENIORITY_LABELS } from "@/lib/constants";

interface DataTableProps {
  jobs: Job[];
}

type SortKey = "title" | "company" | "category" | "seniority" | "lastSeen";
type SortDir = "asc" | "desc";

export default function DataTable({ jobs }: DataTableProps) {
  const [search, setSearch] = useState("");
  const [sortKey, setSortKey] = useState<SortKey>("lastSeen");
  const [sortDir, setSortDir] = useState<SortDir>("desc");
  const [page, setPage] = useState(0);
  const perPage = 25;

  const filtered = useMemo(() => {
    if (!search) return jobs;
    const q = search.toLowerCase();
    return jobs.filter(
      (j) =>
        j.title.toLowerCase().includes(q) ||
        j.company.toLowerCase().includes(q) ||
        j.city.toLowerCase().includes(q) ||
        j.state.toLowerCase().includes(q)
    );
  }, [jobs, search]);

  const sorted = useMemo(() => {
    return [...filtered].sort((a, b) => {
      const aVal = a[sortKey] || "";
      const bVal = b[sortKey] || "";
      const cmp = String(aVal).localeCompare(String(bVal));
      return sortDir === "asc" ? cmp : -cmp;
    });
  }, [filtered, sortKey, sortDir]);

  const pageCount = Math.ceil(sorted.length / perPage);
  const paged = sorted.slice(page * perPage, (page + 1) * perPage);

  function toggleSort(key: SortKey) {
    if (sortKey === key) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir("asc");
    }
    setPage(0);
  }

  const headerClass =
    "px-3 py-2 text-left text-xs font-medium text-slate-500 uppercase cursor-pointer hover:text-slate-800";

  return (
    <div>
      <input
        type="text"
        placeholder="Search jobs..."
        value={search}
        onChange={(e) => {
          setSearch(e.target.value);
          setPage(0);
        }}
        className="w-full px-4 py-2 mb-4 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <div className="overflow-x-auto border border-slate-200 rounded-lg">
        <table className="w-full text-sm">
          <thead className="bg-slate-50">
            <tr>
              <th className={headerClass} onClick={() => toggleSort("title")}>
                Title {sortKey === "title" && (sortDir === "asc" ? "↑" : "↓")}
              </th>
              <th className={headerClass} onClick={() => toggleSort("company")}>
                Company{" "}
                {sortKey === "company" && (sortDir === "asc" ? "↑" : "↓")}
              </th>
              <th className={headerClass} onClick={() => toggleSort("category")}>
                Category{" "}
                {sortKey === "category" && (sortDir === "asc" ? "↑" : "↓")}
              </th>
              <th
                className={headerClass}
                onClick={() => toggleSort("seniority")}
              >
                Seniority{" "}
                {sortKey === "seniority" && (sortDir === "asc" ? "↑" : "↓")}
              </th>
              <th className="px-3 py-2 text-left text-xs font-medium text-slate-500 uppercase">
                Location
              </th>
              <th className={headerClass} onClick={() => toggleSort("lastSeen")}>
                Last Seen{" "}
                {sortKey === "lastSeen" && (sortDir === "asc" ? "↑" : "↓")}
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {paged.map((job, i) => (
              <tr key={i} className="hover:bg-slate-50">
                <td className="px-3 py-2">
                  {job.url ? (
                    <a
                      href={job.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {job.title}
                    </a>
                  ) : (
                    job.title
                  )}
                </td>
                <td className="px-3 py-2">{job.company}</td>
                <td className="px-3 py-2 text-xs">
                  {CATEGORY_LABELS[job.category] || job.category}
                </td>
                <td className="px-3 py-2 text-xs">
                  {SENIORITY_LABELS[job.seniority] || job.seniority}
                </td>
                <td className="px-3 py-2 text-xs">
                  {[job.city, job.state, job.country].filter(Boolean).join(", ")}
                  {job.isRemote && " (Remote)"}
                </td>
                <td className="px-3 py-2 text-xs text-slate-400">
                  {job.lastSeen?.slice(0, 10)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex items-center justify-between mt-3 text-sm text-slate-500">
        <span>
          {sorted.length} jobs
          {search && ` matching "${search}"`}
        </span>
        <div className="flex gap-2">
          <button
            onClick={() => setPage((p) => Math.max(0, p - 1))}
            disabled={page === 0}
            className="px-3 py-1 border rounded disabled:opacity-40"
          >
            Prev
          </button>
          <span className="px-2 py-1">
            {page + 1} / {pageCount || 1}
          </span>
          <button
            onClick={() => setPage((p) => Math.min(pageCount - 1, p + 1))}
            disabled={page >= pageCount - 1}
            className="px-3 py-1 border rounded disabled:opacity-40"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
