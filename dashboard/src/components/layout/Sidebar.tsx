"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV_ITEMS = [
  { href: "/", label: "Overview", icon: "📊" },
  { href: "/trends", label: "Trends", icon: "📈" },
  { href: "/companies", label: "Companies", icon: "🏢" },
  { href: "/categories", label: "Categories", icon: "📁" },
  { href: "/geo", label: "Geography", icon: "🌎" },
  { href: "/jobs", label: "All Jobs", icon: "💼" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-slate-900 text-white min-h-screen p-4 flex flex-col">
      <div className="mb-8">
        <h1 className="text-xl font-bold">AI Job Tracker</h1>
        <p className="text-sm text-slate-400 mt-1">Market Intelligence</p>
      </div>
      <nav className="flex-1 space-y-1">
        {NAV_ITEMS.map((item) => {
          const isActive =
            item.href === "/"
              ? pathname === "/"
              : pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${
                isActive
                  ? "bg-slate-700 text-white"
                  : "text-slate-300 hover:bg-slate-800 hover:text-white"
              }`}
            >
              <span>{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>
      <div className="text-xs text-slate-500 mt-4">
        Powered by Firecrawl
      </div>
    </aside>
  );
}
