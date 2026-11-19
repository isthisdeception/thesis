import React, { useState } from "react";

export function Accordion({ items = [] }) {
  const [openMap, setOpenMap] = useState(() => {
    const initial = {};
    items.forEach((it) => {
      if (it.defaultOpen) initial[it.id] = true;
    });
    return initial;
  });

  const toggle = (id) => {
    setOpenMap((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <div className="divide-y divide-slate-800 rounded-lg border border-slate-800 bg-slate-900/60">
      {items.map((item) => {
        const isOpen = Boolean(openMap[item.id]);
        const regionId = `accordion-region-${item.id}`;
        return (
          <div key={item.id}>
            <button
              type="button"
              aria-expanded={isOpen}
              aria-controls={regionId}
              onClick={() => toggle(item.id)}
              className="flex w-full items-center justify-between px-4 py-3 text-left text-xs font-semibold text-slate-200 hover:bg-slate-800/50"
            >
              <span>{item.title}</span>
              <span className="font-mono text-slate-400">{isOpen ? "−" : "+"}</span>
            </button>
            {isOpen ? (
              <div id={regionId} role="region" className="px-4 pb-3 pt-1 text-xs text-slate-300">
                {item.content}
              </div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
}
