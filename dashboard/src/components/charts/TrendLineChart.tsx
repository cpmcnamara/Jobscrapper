"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import { CATEGORY_COLORS, CATEGORY_LABELS } from "@/lib/constants";
import type { TrendPoint } from "@/lib/types";

interface TrendLineChartProps {
  data: TrendPoint[];
  mode: "total" | "byCategory" | "bySector";
}

export default function TrendLineChart({ data, mode }: TrendLineChartProps) {
  if (mode === "total") {
    return (
      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="date" tick={{ fontSize: 11 }} />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="total"
            stroke="#3b82f6"
            strokeWidth={2}
            dot={false}
            name="Total Jobs"
          />
        </LineChart>
      </ResponsiveContainer>
    );
  }

  if (mode === "byCategory") {
    const categories = new Set<string>();
    data.forEach((d) =>
      Object.keys(d.byCategory).forEach((k) => categories.add(k))
    );
    const flat = data.map((d) => ({ date: d.date, ...d.byCategory }));

    return (
      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={flat}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="date" tick={{ fontSize: 11 }} />
          <YAxis />
          <Tooltip />
          <Legend />
          {Array.from(categories).map((cat) => (
            <Line
              key={cat}
              type="monotone"
              dataKey={cat}
              stroke={CATEGORY_COLORS[cat] || "#94a3b8"}
              strokeWidth={2}
              dot={false}
              name={CATEGORY_LABELS[cat] || cat}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    );
  }

  // bySector
  const flat = data.map((d) => ({ date: d.date, ...d.bySector }));
  return (
    <ResponsiveContainer width="100%" height={350}>
      <LineChart data={flat}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis dataKey="date" tick={{ fontSize: 11 }} />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="consulting"
          stroke="#8b5cf6"
          strokeWidth={2}
          dot={false}
          name="Consulting"
        />
        <Line
          type="monotone"
          dataKey="tech"
          stroke="#3b82f6"
          strokeWidth={2}
          dot={false}
          name="Tech"
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
