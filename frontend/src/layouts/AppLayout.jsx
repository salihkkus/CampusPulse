import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';

export default function AppLayout() {
  return (
    <div className="min-h-screen bg-background text-on-background antialiased">
      <Sidebar />

      <div className="ml-72 flex min-h-screen flex-col">
        <header className="sticky top-0 z-40 flex h-20 w-full items-center justify-between border-b border-white/20 bg-white/70 px-8 shadow-[0_10px_25px_-5px_rgba(0,0,0,0.02)] backdrop-blur-xl dark:bg-slate-900/70 dark:border-slate-800/50">
          <div className="flex flex-1 items-center">
            <div className="relative hidden w-full max-w-md md:block">
              <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
                <span className="material-symbols-outlined text-outline">search</span>
              </div>
              <input
                className="block w-full rounded-full border-transparent bg-surface-container py-2.5 pl-12 pr-4 text-sm placeholder-outline shadow-sm transition-all focus:border-primary focus:bg-white focus:ring-2 focus:ring-primary-fixed-dim"
                placeholder="Search campus devices, rooms..."
                type="text"
              />
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button className="relative rounded-full border border-surface-variant bg-surface-container-low p-2.5 text-slate-500 transition-all duration-200 hover:bg-slate-50 active:scale-95 dark:text-slate-400 dark:hover:bg-slate-800/50">
              <span className="material-symbols-outlined">notifications</span>
              <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-error ring-2 ring-white" />
            </button>
            <button className="rounded-full border border-surface-variant bg-surface-container-low p-2.5 text-slate-500 transition-all duration-200 hover:bg-slate-50 active:scale-95 dark:text-slate-400 dark:hover:bg-slate-800/50">
              <span className="material-symbols-outlined">settings</span>
            </button>
          </div>
        </header>

        <main className="flex-1 space-y-8 overflow-y-auto p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
