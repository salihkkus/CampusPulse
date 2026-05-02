import React from 'react';

export default function MetricCard({ title, value, subtext, icon, iconTone, gradientClass, valueSuffix = '' }) {
  return (
    <div className="glass-card group relative flex min-h-[160px] flex-col justify-between overflow-hidden p-6 cursor-default">
      <div className={`absolute inset-0 z-0 bg-gradient-to-br ${gradientClass} opacity-60`} />
      <div className="relative z-10 flex items-start justify-between">
        <div>
          <p className="mb-1 text-label-sm font-label-sm text-on-surface-variant">{title}</p>
          <div className="flex items-baseline gap-1">
            <h2 className="font-display text-display text-on-surface">{value}{valueSuffix}</h2>
          </div>
        </div>
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-white bg-white shadow-sm">
          <span className={`material-symbols-outlined ${iconTone}`} style={{ fontVariationSettings: "'FILL' 1" }}>
            {icon}
          </span>
        </div>
      </div>
      <div className="relative z-10 mt-4 flex items-center gap-2">
        <span className="text-xs font-medium text-on-surface-variant">{subtext}</span>
      </div>
    </div>
  );
}
