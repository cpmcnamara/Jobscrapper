"use client";

import { useEffect, useState } from "react";
import { fetchGeo } from "@/lib/api";
import StatCard from "@/components/data/StatCard";

interface GeoData {
  locations: {
    country: string;
    state: string;
    city: string;
    isRemote: boolean;
    company: string;
    category: string;
    count: number;
  }[];
  remoteTotal: number;
  topCountries: { country: string; count: number }[];
}

export default function GeoPage() {
  const [data, setData] = useState<GeoData | null>(null);

  useEffect(() => {
    fetchGeo()
      .then(setData)
      .catch(() => {});
  }, []);

  if (!data) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-slate-400">Loading...</p>
      </div>
    );
  }

  // Aggregate by state
  const stateMap = new Map<string, number>();
  const cityMap = new Map<string, number>();
  let totalJobs = 0;

  for (const loc of data.locations) {
    totalJobs += loc.count;
    if (loc.state) {
      stateMap.set(loc.state, (stateMap.get(loc.state) || 0) + loc.count);
    }
    if (loc.city) {
      const key = loc.city + (loc.state ? `, ${loc.state}` : "");
      cityMap.set(key, (cityMap.get(key) || 0) + loc.count);
    }
  }

  const topStates = [...stateMap.entries()]
    .sort(([, a], [, b]) => b - a)
    .slice(0, 15);
  const topCities = [...cityMap.entries()]
    .sort(([, a], [, b]) => b - a)
    .slice(0, 15);

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-2">
        Geographic Distribution
      </h1>
      <p className="text-sm text-slate-500 mb-6">
        Where AI &amp; data roles are concentrated
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <StatCard label="Total Jobs" value={totalJobs} />
        <StatCard label="Remote Jobs" value={data.remoteTotal} color="#10b981" />
        <StatCard
          label="Countries"
          value={data.topCountries.length}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">
            Top Countries
          </h2>
          <div className="space-y-3">
            {data.topCountries.map((c) => (
              <div key={c.country} className="flex items-center justify-between">
                <span className="text-sm text-slate-700">{c.country}</span>
                <div className="flex items-center gap-2">
                  <div className="w-32 bg-slate-100 rounded-full h-2.5">
                    <div
                      className="h-2.5 bg-blue-500 rounded-full"
                      style={{
                        width: `${Math.min(100, (c.count / (data.topCountries[0]?.count || 1)) * 100)}%`,
                      }}
                    />
                  </div>
                  <span className="text-xs text-slate-500 w-10 text-right">
                    {c.count}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">
            Top States / Provinces
          </h2>
          <div className="space-y-3">
            {topStates.map(([state, count]) => (
              <div key={state} className="flex items-center justify-between">
                <span className="text-sm text-slate-700">{state}</span>
                <div className="flex items-center gap-2">
                  <div className="w-32 bg-slate-100 rounded-full h-2.5">
                    <div
                      className="h-2.5 bg-purple-500 rounded-full"
                      style={{
                        width: `${Math.min(100, (count / (topStates[0]?.[1] || 1)) * 100)}%`,
                      }}
                    />
                  </div>
                  <span className="text-xs text-slate-500 w-10 text-right">
                    {count}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-800 mb-4">
          Top Cities
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {topCities.map(([city, count]) => (
            <div
              key={city}
              className="flex items-center justify-between bg-slate-50 rounded-lg px-4 py-2"
            >
              <span className="text-sm text-slate-700">{city}</span>
              <span className="text-sm font-medium text-slate-900">
                {count}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
