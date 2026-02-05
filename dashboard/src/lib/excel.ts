import ExcelJS from "exceljs";
import type { Job } from "./types";
import { CATEGORY_LABELS, SENIORITY_LABELS } from "./constants";

export async function exportToExcel(jobs: Job[], filename?: string) {
  const workbook = new ExcelJS.Workbook();
  workbook.creator = "AI Job Market Tracker";

  // Sheet 1: All Jobs
  const sheet = workbook.addWorksheet("Jobs");
  sheet.columns = [
    { header: "Title", key: "title", width: 40 },
    { header: "Company", key: "company", width: 20 },
    { header: "Sector", key: "sector", width: 12 },
    { header: "Category", key: "category", width: 30 },
    { header: "Seniority", key: "seniority", width: 12 },
    { header: "City", key: "city", width: 18 },
    { header: "State", key: "state", width: 18 },
    { header: "Country", key: "country", width: 18 },
    { header: "Remote", key: "isRemote", width: 8 },
    { header: "URL", key: "url", width: 50 },
    { header: "First Seen", key: "firstSeen", width: 14 },
    { header: "Last Seen", key: "lastSeen", width: 14 },
  ];

  // Header styling
  sheet.getRow(1).font = { bold: true };
  sheet.getRow(1).fill = {
    type: "pattern",
    pattern: "solid",
    fgColor: { argb: "FF1E293B" },
  };
  sheet.getRow(1).font = { bold: true, color: { argb: "FFFFFFFF" } };

  for (const job of jobs) {
    sheet.addRow({
      ...job,
      category: CATEGORY_LABELS[job.category] || job.category,
      seniority: SENIORITY_LABELS[job.seniority] || job.seniority,
      isRemote: job.isRemote ? "Yes" : "No",
      firstSeen: job.firstSeen?.slice(0, 10) || "",
      lastSeen: job.lastSeen?.slice(0, 10) || "",
    });
  }

  // Sheet 2: Summary by Company
  const summarySheet = workbook.addWorksheet("Summary by Company");
  const companyMap = new Map<string, { sector: string; count: number }>();
  for (const job of jobs) {
    const existing = companyMap.get(job.company) || {
      sector: job.sector,
      count: 0,
    };
    existing.count++;
    companyMap.set(job.company, existing);
  }
  summarySheet.columns = [
    { header: "Company", key: "company", width: 25 },
    { header: "Sector", key: "sector", width: 12 },
    { header: "Active Jobs", key: "count", width: 14 },
  ];
  summarySheet.getRow(1).font = { bold: true };
  for (const [company, data] of companyMap) {
    summarySheet.addRow({ company, ...data });
  }

  // Sheet 3: Summary by Category
  const catSheet = workbook.addWorksheet("Summary by Category");
  const catMap = new Map<string, number>();
  for (const job of jobs) {
    catMap.set(job.category, (catMap.get(job.category) || 0) + 1);
  }
  catSheet.columns = [
    { header: "Category", key: "category", width: 35 },
    { header: "Job Count", key: "count", width: 14 },
  ];
  catSheet.getRow(1).font = { bold: true };
  for (const [cat, count] of catMap) {
    catSheet.addRow({
      category: CATEGORY_LABELS[cat] || cat,
      count,
    });
  }

  // Generate and download
  const buffer = await workbook.xlsx.writeBuffer();
  const blob = new Blob([buffer], {
    type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename || `ai-jobs-${new Date().toISOString().slice(0, 10)}.xlsx`;
  a.click();
  URL.revokeObjectURL(url);
}
