import React from 'react';
import ThreeDMap from '../components/ThreeDMap';

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
          <ThreeDMap />
        </div>
      </div>
    </div>
  );
}
