"use client";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { CATEGORY_LABELS, CATEGORY_COLORS } from "@/lib/constants";

interface CategoryDonutProps {
  data: Record<string, number>;
}

export default function CategoryDonut({ data }: CategoryDonutProps) {
  const chartData = Object.entries(data)
    .map(([key, value]) => ({
      name: CATEGORY_LABELS[key] || key,
      value,
      color: CATEGORY_COLORS[key] || "#94a3b8",
    }))
    .sort((a, b) => b.value - a.value);

  return (
    <ResponsiveContainer width="100%" height={350}>
      <PieChart>
        <Pie
          data={chartData}
          cx="50%"
          cy="50%"
          innerRadius={70}
          outerRadius={120}
          dataKey="value"
          label={
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            ((props: any) =>
              `${props.name ?? ""} (${(((props.percent as number) ?? 0) * 100).toFixed(0)}%)`) as any
          }
          labelLine
        >
          {chartData.map((entry, i) => (
            <Cell key={i} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  );
}
