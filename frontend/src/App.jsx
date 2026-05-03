import React from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import AppLayout from './layouts/AppLayout';
import DashboardPage from './pages/DashboardPage';
import LiveMapPage from './pages/LiveMapPage';
import RoomsPage from './pages/RoomsPage';
import ReportsPage from './pages/ReportsPage';
import LandingPage from './pages/LandingPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Landing Page — sidebar'sız */}
        <Route path="/" element={<LandingPage />} />

        {/* Dashboard — sidebar'lı layout */}
        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/dashboard/rooms" element={<RoomsPage />} />
          <Route path="/dashboard/live-map" element={<LiveMapPage />} />
          <Route path="/dashboard/reports" element={<ReportsPage />} />
        </Route>

        {/* Eski path'lerden yeni path'lere yönlendir */}
        <Route path="/rooms" element={<Navigate to="/dashboard/rooms" replace />} />
        <Route path="/live-map" element={<Navigate to="/dashboard/live-map" replace />} />
        <Route path="/reports" element={<Navigate to="/dashboard/reports" replace />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
