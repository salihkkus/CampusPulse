import React from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import AppLayout from './layouts/AppLayout';
import DashboardPage from './pages/DashboardPage';
import PlaceholderPage from './pages/PlaceholderPage';
import ReportsPage from './pages/ReportsPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<DashboardPage />} />
          <Route
            path="/live-map"
            element={
              <PlaceholderPage
                title="3D Live Map"
                description="Bu sayfa için ayrı bir React component hazır. Burada canlı kampüs haritası ve 3D görünüm eklenecek."
              />
            }
          />
          <Route
            path="/reports"
            element={<ReportsPage />}
          />
          <Route
            path="/schedules"
            element={
              <PlaceholderPage
                title="Schedules"
                description="Zamanlama ekranı için ayrı sayfa hazır. Sidebar bu sayfada da aynı layout üzerinden görünür."
              />
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
