import React from 'react';
import { NavLink } from 'react-router-dom';
import { navigationItems } from '../data/mockData';

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 z-50 flex h-screen w-72 flex-col gap-8 border-r border-slate-100 bg-white p-6 text-sm font-medium text-indigo-600 shadow-none dark:border-slate-800 dark:bg-slate-950 dark:text-indigo-400">
      <div className="flex items-center gap-4 px-4">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary shadow-sm">
          <span className="material-symbols-outlined text-white" style={{ fontVariationSettings: "'FILL' 1" }}>
            domain
          </span>
        </div>
        <div>
          <h1 className="bg-gradient-to-r from-cyan-500 to-indigo-500 bg-clip-text text-2xl font-black tracking-tight text-transparent">
            CampusPulse
          </h1>
          <p className="text-xs font-medium text-slate-500">Yönetici Paneli</p>
        </div>
      </div>

      <nav className="mt-4 flex flex-1 flex-col gap-2">
        {navigationItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.end}
            className={({ isActive }) =>
              [
                'flex items-center gap-4 rounded-2xl px-4 py-3 transition-transform duration-200 active:scale-95',
                isActive
                  ? 'bg-indigo-50 text-indigo-600 dark:bg-indigo-900/20 dark:text-indigo-400'
                  : 'text-slate-500 hover:translate-x-1 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100',
              ].join(' ')
            }
          >
            <span className="material-symbols-outlined" style={item.end ? { fontVariationSettings: "'FILL' 1" } : undefined}>
              {item.icon}
            </span>
            {item.label}
          </NavLink>
        ))}
      </nav>

    </aside>
  );
}
