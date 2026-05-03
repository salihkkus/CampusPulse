import React, { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import RoomStatusCard from '../components/RoomStatusCard';
import { useApi } from '../hooks/useApi';
import { getBatchAnalysis } from '../services/api';

const STATUS_FILTERS = [
  { key: 'ALL',       label: 'Tümü',      icon: 'apps',          color: 'bg-surface-container text-on-surface' },
  { key: 'CRITICAL',  label: 'Kritik',     icon: 'error',         color: 'bg-red-100 text-red-700' },
  { key: 'NORMAL',    label: 'Normal',     icon: 'check_circle',  color: 'bg-emerald-100 text-emerald-700' },
];

const CRITICAL_STATUSES = new Set(['CRITICAL', 'WARNING', 'ATTENTION', 'ANOMALY']);
const NORMAL_STATUSES = new Set(['NORMAL', 'ACTIVE']);

export default function RoomsPage() {
  const navigate = useNavigate();
  const [activeFilter, setActiveFilter] = useState('ALL');

  const { data: batchData, loading } = useApi(getBatchAnalysis, [], 30_000);
  const rooms = batchData?.data?.rooms || [];

  // Durum sayılarını hesapla (badge'ler için)
  const statusCounts = useMemo(() => {
    const counts = { ALL: rooms.length, CRITICAL: 0, NORMAL: 0 };
    rooms.forEach(r => {
      const s = r?.status ?? 'NORMAL';
      if (CRITICAL_STATUSES.has(s)) counts.CRITICAL++;
      else counts.NORMAL++;
    });
    return counts;
  }, [rooms]);

  // Filtrelenmiş ve sıralanmış odalar
  const filteredRooms = useMemo(() => {
    let list = rooms;
    if (activeFilter === 'CRITICAL') {
      list = rooms.filter(r => CRITICAL_STATUSES.has(r?.status ?? 'NORMAL'));
    } else if (activeFilter === 'NORMAL') {
      list = rooms.filter(r => NORMAL_STATUSES.has(r?.status ?? 'NORMAL'));
    }
    // Kritik olanlar başa
    const priority = { CRITICAL: 0, WARNING: 1, ATTENTION: 2, ANOMALY: 3, ACTIVE: 4, NORMAL: 5 };
    return [...list].sort((a, b) => (priority[a.status] ?? 5) - (priority[b.status] ?? 5));
  }, [rooms, activeFilter]);

  return (
    <div className="mx-auto flex w-full max-w-7xl flex-col gap-lg">
      <header className="mb-2 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <button 
            onClick={() => navigate(-1)} 
            className="mb-2 flex items-center gap-1 text-sm font-medium text-primary hover:underline"
          >
            <span className="material-symbols-outlined text-[16px]">arrow_back</span>
            Gösterge Paneline Dön
          </button>
          <h1 className="font-h1 text-h1 text-on-surface">Oda Durumları (Canlı)</h1>
          <p className="font-body-md text-on-surface-variant">Tüm izlenen odalar için canlı enerji takibi.</p>
        </div>
        <div className="flex items-center gap-2 rounded-xl bg-emerald-50 px-4 py-2 text-sm text-emerald-700 shadow-sm">
          <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          {rooms.length} oda izleniyor
        </div>
      </header>

      {/* ── Durum Filtreleri ─────────────────────────── */}
      <div className="flex flex-wrap items-center gap-2">
        {STATUS_FILTERS.map(f => {
          const count = statusCounts[f.key] ?? 0;
          const isActive = activeFilter === f.key;
          return (
            <button
              key={f.key}
              onClick={() => setActiveFilter(f.key)}
              className={`
                flex items-center gap-1.5 rounded-full px-3.5 py-2 text-xs font-semibold
                transition-all duration-200
                ${isActive 
                  ? `${f.color} ring-2 ring-offset-1 ring-primary/40 shadow-sm scale-[1.03]` 
                  : 'bg-surface-container-low text-on-surface-variant hover:bg-surface-container hover:shadow-sm'
                }
              `}
            >
              <span className="material-symbols-outlined text-[16px]">{f.icon}</span>
              {f.label}
              <span className={`
                ml-0.5 min-w-[20px] rounded-full px-1.5 py-0.5 text-[10px] font-bold leading-none
                ${isActive ? 'bg-white/40' : 'bg-surface-container'}
              `}>
                {count}
              </span>
            </button>
          );
        })}
      </div>

      {/* ── Sonuç Bilgisi ──────────────────────────── */}
      {activeFilter !== 'ALL' && (
        <div className="flex items-center gap-2 text-sm text-on-surface-variant">
          <span className="material-symbols-outlined text-[16px]">filter_list</span>
          <span>
            <strong className="text-on-surface">{filteredRooms.length}</strong> oda gösteriliyor
            {' '}({STATUS_FILTERS.find(f => f.key === activeFilter)?.label} filtresi aktif)
          </span>
          <button
            onClick={() => setActiveFilter('ALL')}
            className="ml-1 rounded-full bg-surface-container px-2.5 py-0.5 text-xs font-medium text-primary hover:bg-primary/10 transition-colors"
          >
            Filtreyi Kaldır
          </button>
        </div>
      )}

      {/* ── Oda Kartları ───────────────────────────── */}
      {loading && rooms.length === 0 ? (
        <div className="flex h-64 items-center justify-center rounded-2xl border border-surface-container bg-surface-container-lowest">
          <div className="flex flex-col items-center gap-2">
            <span className="material-symbols-outlined animate-spin text-4xl text-primary">autorenew</span>
            <p className="text-on-surface-variant">Oda durumları yükleniyor...</p>
          </div>
        </div>
      ) : filteredRooms.length > 0 ? (
        <section className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3 items-start">
          {filteredRooms.map((room) => (
            <RoomStatusCard key={room.room_id} room={room} />
          ))}
        </section>
      ) : (
        <div className="flex h-48 flex-col items-center justify-center rounded-2xl border border-surface-container bg-surface-container-lowest text-on-surface-variant">
          <span className="material-symbols-outlined text-[48px] mb-3 opacity-50">search_off</span>
          <p className="font-medium">Bu filtreye uygun oda bulunamadı.</p>
          <button
            onClick={() => setActiveFilter('ALL')}
            className="mt-3 rounded-full bg-primary px-4 py-2 text-xs font-semibold text-on-primary hover:bg-primary/90 transition-colors"
          >
            Tüm Odaları Göster
          </button>
        </div>
      )}
    </div>
  );
}
