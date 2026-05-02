import React from 'react';
import { useNavigate } from 'react-router-dom';
import RoomStatusCard from '../components/RoomStatusCard';
import { useApi } from '../hooks/useApi';
import { getBatchAnalysis } from '../services/api';

export default function RoomsPage() {
  const navigate = useNavigate();
  const { data: batchData, loading } = useApi(getBatchAnalysis, [], 30_000);
  const rooms = batchData?.data?.rooms || [];

  return (
    <div className="mx-auto flex w-full max-w-7xl flex-col gap-lg">
      <header className="mb-6 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
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

      {loading && rooms.length === 0 ? (
        <div className="flex h-64 items-center justify-center rounded-2xl border border-surface-container bg-surface-container-lowest">
          <div className="flex flex-col items-center gap-2">
            <span className="material-symbols-outlined animate-spin text-4xl text-primary">autorenew</span>
            <p className="text-on-surface-variant">Oda durumları yükleniyor...</p>
          </div>
        </div>
      ) : (
        <section className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
          {rooms.map((room) => (
            <RoomStatusCard key={room.room_id} room={room} />
          ))}
        </section>
      )}
    </div>
  );
}
