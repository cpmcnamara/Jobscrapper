"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { SENIORITY_ORDER, SENIORITY_LABELS } from "@/lib/constants";

interface SeniorityStackProps {
  data: Record<string, number>;
}

const COLORS = [
  "#cbd5e1", "#94a3b8", "#64748b", "#475569",
  "#334155", "#1e293b", "#0f172a", "#6366f1", "#4f46e5",
];

export default function SeniorityStack({ data }: SeniorityStackProps) {
  const chartData = SENIORITY_ORDER
    .filter((s) => data[s])
    .map((s) => ({
      name: SENIORITY_LABELS[s] || s,
      value: data[s] || 0,
    }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData}>
        <XAxis dataKey="name" tick={{ fontSize: 11 }} />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value" fill="#6366f1" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
