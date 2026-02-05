"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { SECTOR_COLORS } from "@/lib/constants";

interface CompanyBarChartProps {
  data: { name: string; value: number; sector: string }[];
}

export default function CompanyBarChart({ data }: CompanyBarChartProps) {
  const sorted = [...data].sort((a, b) => b.value - a.value);

  return (
    <ResponsiveContainer width="100%" height={Math.max(300, sorted.length * 36)}>
      <BarChart data={sorted} layout="vertical" margin={{ left: 100 }}>
        <XAxis type="number" />
        <YAxis
          type="category"
          dataKey="name"
          width={95}
          tick={{ fontSize: 12 }}
        />
        <Tooltip />
        <Bar dataKey="value" radius={[0, 4, 4, 0]}>
          {sorted.map((entry, i) => (
            <Cell
              key={i}
              fill={SECTOR_COLORS[entry.sector] || "#64748b"}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
