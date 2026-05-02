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
          <p className="text-xs font-medium text-slate-500">Admin Console</p>
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

      <div className="mt-auto">
        <div className="flex cursor-pointer items-center gap-3 rounded-2xl border border-surface-variant bg-surface-container-low p-4 transition-colors hover:bg-surface-container-high">
          <img
            alt="Admin User Profile"
            className="h-10 w-10 rounded-full border-2 border-white shadow-sm"
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuBRivF9eUCyh0lL4TQOxe_TtQY4Mqryzr1F2lztSzYgHWk9JJL4CxskWSCxCvHWW0SAzUm6L3f_FrODVDFyiOoVYD9ceSpNjEhN-EPZsvG4jW3qAy2Yb7I_C1fjNKsaPpi77yfsPqQk-vonfyIiXHBt9CHAtcKdZKTS3F7FqtItPDpKCagRA7r70qSl0zD7HJ970-CwbUubwEq-em06MPUPKgFvU6DcR7btjag3WauWfwwjdQXsOUtRxiOEfibgGDcwv3JQkQfUFtlq"
          />
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-semibold text-on-surface">Admin User</p>
            <p className="truncate text-xs text-on-surface-variant">System Manager</p>
          </div>
          <span className="material-symbols-outlined text-outline">more_vert</span>
        </div>
      </div>
    </aside>
  );
}
