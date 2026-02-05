interface StatCardProps {
  label: string;
  value: string | number;
  subtitle?: string;
  color?: string;
}

export default function StatCard({ label, value, subtitle, color }: StatCardProps) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <p className="text-sm text-slate-500 font-medium">{label}</p>
      <p
        className="text-3xl font-bold mt-1"
        style={color ? { color } : undefined}
      >
        {typeof value === "number" ? value.toLocaleString() : value}
      </p>
      {subtitle && (
        <p className="text-sm text-slate-400 mt-1">{subtitle}</p>
      )}
    </div>
  );
}
