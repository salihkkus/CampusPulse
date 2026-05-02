import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';

export default function AppLayout() {
  return (
    <div className="min-h-screen bg-background text-on-background antialiased">
      <Sidebar />

      <div className="ml-72 flex min-h-screen flex-col">


        <main className="flex-1 space-y-8 overflow-y-auto p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
