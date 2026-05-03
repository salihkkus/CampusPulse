import React from 'react';

export default function MetricCard({ title, value, subtext, icon, iconTone, gradientClass, valueSuffix = '' }) {
  return (
    <div className="glass-card group relative flex min-h-[190px] flex-col justify-between overflow-hidden p-6 cursor-default transition-all duration-300 hover:scale-[1.02] hover:shadow-lg">
      <div className={`absolute inset-0 z-0 bg-gradient-to-br ${gradientClass} opacity-60 transition-opacity group-hover:opacity-80`} />
      <div className="relative z-10 flex items-start justify-between">
        <div>
          <p className="mb-2 text-label-sm font-label-sm text-on-surface-variant/80 tracking-wider">{title}</p>
          <div className="flex items-baseline gap-1">
            <h2 className="font-display text-3xl font-bold text-on-surface lg:text-4xl">{value}<span className="ml-1 text-lg font-semibold opacity-60">{valueSuffix}</span></h2>
          </div>
        </div>
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-white/50 bg-white/80 shadow-sm backdrop-blur-sm transition-transform group-hover:rotate-12">
          <span className={`material-symbols-outlined ${iconTone} text-3xl`} style={{ fontVariationSettings: "'FILL' 1" }}>
            {icon}
          </span>
        </div>
      </div>
      <div className="relative z-10 mt-4 flex items-center gap-2">
        <div className="h-1 w-1 rounded-full bg-on-surface-variant/30" />
        <span className="text-xs font-medium text-on-surface-variant/70">{subtext}</span>
      </div>
    </div>
  );
}
