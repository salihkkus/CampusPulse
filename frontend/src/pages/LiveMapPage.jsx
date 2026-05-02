import React from 'react';

export default function LiveMapPage() {
  return (
    <div className="mx-auto flex h-full max-w-7xl flex-col gap-lg">
      <header>
        <h1 className="mb-xs font-h1 text-h1 text-on-background">3D Live Map</h1>
        <p className="font-body-lg text-body-lg text-on-surface-variant">
          Interactive campus thermal and energy analysis.
        </p>
      </header>

      {/* The 3D Viewer Card */}
      <div className="flex flex-1 flex-col rounded-3xl border border-outline-variant/30 bg-surface-container-lowest p-6 shadow-[0_10px_25px_-5px_rgba(0,0,0,0.02),0_8px_10px_-6px_rgba(0,0,0,0.02)] md:p-8">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h2 className="font-h2 text-h2 text-on-background">Live 3D Digital Twin</h2>
            <p className="font-body-md text-body-md text-on-surface-variant">
              Real-time thermal and energy mapping
            </p>
          </div>
          <div className="flex items-center gap-2 rounded-full border border-error-container bg-error-container/50 px-3 py-1.5 font-label-sm text-on-error-container backdrop-blur-sm">
            <span className="h-2 w-2 animate-pulse rounded-full bg-error"></span>
            • High Consumption
          </div>
        </div>

        <div className="relative flex min-h-[600px] flex-1 flex-col items-center justify-center overflow-hidden rounded-2xl border border-outline-variant/50 bg-surface-container">
          {/* Decorative grid background to imply 3D space */}
          <div
            className="absolute inset-0 opacity-10"
            style={{
              backgroundImage: 'radial-gradient(#767586 1px, transparent 1px)',
              backgroundSize: '32px 32px',
            }}
          ></div>

          <div className="relative z-10 flex max-w-md flex-col items-center gap-6 rounded-2xl border border-outline-variant/30 bg-surface-container-lowest/80 p-6 text-center shadow-sm backdrop-blur-xl">
            <span className="material-symbols-outlined text-4xl text-primary" data-icon="domain">
              domain
            </span>
            <p className="font-body-md text-body-md text-on-surface-variant">
              Three.js 3D Campus Model Will Mount Here.
              <br />
              Red lights will indicate high consumption areas.
            </p>
            <button className="rounded-xl bg-gradient-to-r from-primary to-surface-tint px-6 py-3 font-label-sm text-on-primary shadow-[0_8px_16px_-4px_rgba(70,72,212,0.3)] transition-all duration-300 hover:-translate-y-0.5 hover:shadow-[0_12px_20px_-4px_rgba(70,72,212,0.4)]">
              Initialize Viewer
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
