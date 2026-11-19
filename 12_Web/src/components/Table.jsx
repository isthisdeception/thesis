import React from "react";

export function Table({ columns = [], rows = [], caption = "", emptyMessage = "No records available." }) {
  return (
    <div className="overflow-x-auto rounded-lg border border-slate-800">
      <table className="min-w-full divide-y divide-slate-800 text-left text-xs">
        {caption ? <caption className="sr-only">{caption}</caption> : null}
        <thead className="bg-slate-900 text-slate-300">
          <tr>
            {columns.map((col) => (
              <th key={col.key} scope="col" className="px-3 py-2 font-semibold">
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800 bg-slate-950/60 text-slate-200">
          {rows.length === 0 ? (
            <tr>
              <td colSpan={Math.max(1, columns.length)} className="px-3 py-4 text-center text-slate-400">
                {emptyMessage}
              </td>
            </tr>
          ) : (
            rows.map((row, rIdx) => (
              <tr key={row.id || rIdx} className="hover:bg-slate-900/50">
                {columns.map((col) => (
                  <td key={col.key} className="px-3 py-2 align-top">
                    {col.render ? col.render(row) : row[col.key] ?? "—"}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
