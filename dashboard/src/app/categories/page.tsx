"use client";

import { useEffect, useState } from "react";
import CategoryDonut from "@/components/charts/CategoryDonut";
import SeniorityStack from "@/components/charts/SeniorityStack";
import { fetchCategories } from "@/lib/api";
import type { CategoryData } from "@/lib/types";
import { CATEGORY_COLORS } from "@/lib/constants";

export default function CategoriesPage() {
  const [categories, setCategories] = useState<CategoryData[]>([]);

  useEffect(() => {
    fetchCategories().then((d) => setCategories(d.categories)).catch(() => {});
  }, []);

  const overview: Record<string, number> = {};
  categories.forEach((c) => {
    overview[c.id] = c.totalJobs;
  });

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-2">
        Role Categories
      </h1>
      <p className="text-sm text-slate-500 mb-6">
        How AI &amp; data roles break down by focus area
      </p>

      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm mb-8">
        <h2 className="text-lg font-semibold text-slate-800 mb-4">
          Overall Distribution
        </h2>
        <CategoryDonut data={overview} />
      </div>

      <div className="space-y-6">
        {categories.map((cat) => (
          <div
            key={cat.id}
            className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm"
          >
            <div className="flex items-center gap-3 mb-4">
              <div
                className="w-3 h-3 rounded-full"
                style={{
                  backgroundColor: CATEGORY_COLORS[cat.id] || "#94a3b8",
                }}
              />
              <h3 className="text-lg font-semibold text-slate-800">
                {cat.name}
              </h3>
              <span className="text-sm text-slate-400">
                {cat.totalJobs} jobs
              </span>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div>
                <p className="text-xs font-medium text-slate-500 mb-2">
                  Seniority Distribution
                </p>
                <SeniorityStack data={cat.bySeniority} />
              </div>
              <div>
                <p className="text-xs font-medium text-slate-500 mb-2">
                  Top Companies
                </p>
                <div className="space-y-2">
                  {Object.entries(cat.byCompany)
                    .sort(([, a], [, b]) => b - a)
                    .slice(0, 8)
                    .map(([company, count]) => (
                      <div
                        key={company}
                        className="flex items-center justify-between"
                      >
                        <span className="text-sm text-slate-600">
                          {company}
                        </span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-slate-100 rounded-full h-2">
                            <div
                              className="h-2 rounded-full"
                              style={{
                                width: `${Math.min(100, (count / cat.totalJobs) * 100)}%`,
                                backgroundColor:
                                  CATEGORY_COLORS[cat.id] || "#94a3b8",
                              }}
                            />
                          </div>
                          <span className="text-xs text-slate-400 w-8 text-right">
                            {count}
                          </span>
                        </div>
                      </div>
                    ))}
                </div>
                {cat.topTitles.length > 0 && (
                  <div className="mt-4">
                    <p className="text-xs font-medium text-slate-500 mb-2">
                      Most Common Titles
                    </p>
                    <ul className="text-xs text-slate-600 space-y-1">
                      {cat.topTitles.slice(0, 5).map((t, i) => (
                        <li key={i}>
                          {t.title}{" "}
                          <span className="text-slate-400">({t.count})</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
