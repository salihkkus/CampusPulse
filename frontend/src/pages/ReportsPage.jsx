import React from 'react';
import { useApi } from '../hooks/useApi';
import { getEnergyAuditReport, getBatchAnalysis } from '../services/api';

function getStatusClass(status) {
  if (status === 'CRITICAL') return 'bg-error-container text-on-error-container';
  if (status === 'WARNING' || status === 'ATTENTION') return 'bg-[#fef9c3] text-[#854d0e]';
  if (status === 'NORMAL' || status === 'ACTIVE') return 'bg-[#dcfce7] text-[#166534]';
  return 'bg-[#e0e7ff] text-[#3730a3]';
}

export default function ReportsPage() {
  const { data: batchData, loading } = useApi(getBatchAnalysis, [], 30_000);
  const rooms = batchData?.data?.rooms || [];
  const summary = batchData?.data?.summary || {};

  // Build carbon data per room
  const carbonData = rooms.map((r) => ({
    label: r.room_id,
    value: r?.analysis?.financial?.daily_carbon ?? 0,
  }));

  const maxCarbon = Math.max(...carbonData.map((d) => d.value), 1);

  // Build anomaly log from rooms
  const anomalies = rooms
    .filter((r) => r.status !== 'NORMAL' && r.status !== 'ACTIVE')
    .map((r) => ({
      dateTime: r.timestamp,
      roomId: r.room_id,
      device: r.current_data?.detected_devices?.join(', ') || '-',
      wastedPowerKw: ((r.current_data?.power_consumption ?? 0) / 1000).toFixed(2),
      financialLossTl: (r.analysis?.financial?.daily_cost ?? 0).toFixed(2),
      status: r.status,
    }));

  // Summary stats
  const totalWasteCostHour = summary.total_waste_cost ?? 0;
  const totalSavings = summary.total_potential_savings ?? 0;

  return (
    <div className="mx-auto flex w-full max-w-7xl flex-col gap-lg">
      {/* Header */}
      <section className="mb-2 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
        <h1 className="font-h1 text-h1 text-on-surface">Enerji &amp; Finansal Raporlar</h1>

        <div className="flex flex-wrap items-center gap-3">
          <button onClick={() => alert('PDF rapor oluşturma başlatıldı.')} className="flex items-center gap-2 rounded-xl border border-surface-variant bg-surface-container-lowest px-4 py-2.5 font-label-sm text-label-sm text-on-surface-variant shadow-[0_2px_10px_-2px_rgba(0,0,0,0.02)] transition-all hover:-translate-y-px hover:shadow-[0_4px_12px_-2px_rgba(0,0,0,0.05)]">
            <span className="material-symbols-outlined text-[18px]">file_copy</span>
            PDF Dışa Aktar
          </button>
          <button onClick={() => alert('CSV indiriliyor...')} className="flex items-center gap-2 rounded-xl border border-surface-variant bg-surface-container-lowest px-4 py-2.5 font-label-sm text-label-sm text-on-surface-variant shadow-[0_2px_10px_-2px_rgba(0,0,0,0.02)] transition-all hover:-translate-y-px hover:shadow-[0_4px_12px_-2px_rgba(0,0,0,0.05)]">
            <span className="material-symbols-outlined text-[18px]">download</span>
            CSV İndir
          </button>
        </div>
      </section>

      {/* Live Summary Cards */}
      <section className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <SummaryCard
          label="Toplam Oda"
          value={summary.total_rooms ?? 0}
          icon="meeting_room"
          color="text-indigo-600"
          bg="bg-indigo-50"
        />
        <SummaryCard
          label="İsraf Yapan Oda"
          value={summary.wasting_rooms ?? 0}
          icon="warning"
          color="text-red-600"
          bg="bg-red-50"
        />
        <SummaryCard
          label="Saatlik İsraf"
          value={`₺${totalWasteCostHour.toFixed(2)}`}
          icon="payments"
          color="text-orange-600"
          bg="bg-orange-50"
        />
        <SummaryCard
          label="Aylık Tasarruf"
          value={`₺${totalSavings.toFixed(0)}`}
          icon="savings"
          color="text-emerald-600"
          bg="bg-emerald-50"
        />
      </section>

      {/* Charts Row */}
      <section className="grid grid-cols-1 gap-lg lg:grid-cols-2">
        {/* Carbon per room */}
        <article className="rounded-[32px] border border-surface-container-highest bg-surface-container-lowest p-md shadow-[0_8px_30px_rgb(0,0,0,0.04)] transition-all duration-300 hover:-translate-y-[2px] hover:shadow-[0_12px_40px_rgb(0,0,0,0.06)] lg:p-lg">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="font-h2 text-h2 text-on-surface">Oda Bazlı Günlük Karbon (kg CO₂)</h2>
            <span className="material-symbols-outlined text-outline">more_horiz</span>
          </div>

          <div className="relative flex h-[250px] w-full items-end justify-between gap-2 px-2 pb-6">
            {loading && (
              <div className="flex h-full w-full items-center justify-center text-on-surface-variant">
                Yükleniyor...
              </div>
            )}
            {!loading &&
              carbonData.map((item) => {
                const height = `${Math.round((item.value / maxCarbon) * 100)}%`;
                return (
                  <div key={item.label} className="flex w-full flex-col items-center gap-2">
                    <div className="group relative w-full rounded-t-lg bg-[#10b981]/30" style={{ height: height || '2%' }}>
                      <div className="absolute -top-8 left-1/2 -translate-x-1/2 rounded bg-inverse-surface px-2 py-1 text-xs text-inverse-on-surface opacity-0 transition-opacity group-hover:opacity-100">
                        {item.value.toFixed(1)}
                      </div>
                    </div>
                    <span className="font-caption text-caption text-outline">{item.label}</span>
                  </div>
                );
              })}
            <div className="absolute bottom-6 left-0 w-full border-b border-surface-variant" />
            <div className="absolute bottom-[calc(6px+25%)] left-0 w-full border-b border-dashed border-surface-variant" />
            <div className="absolute bottom-[calc(6px+50%)] left-0 w-full border-b border-dashed border-surface-variant" />
            <div className="absolute bottom-[calc(6px+75%)] left-0 w-full border-b border-dashed border-surface-variant" />
          </div>
        </article>

        {/* Wasted Cost per room */}
        <article className="rounded-[32px] border border-surface-container-highest bg-surface-container-lowest p-md shadow-[0_8px_30px_rgb(0,0,0,0.04)] transition-all duration-300 hover:-translate-y-[2px] hover:shadow-[0_12px_40px_rgb(0,0,0,0.06)] lg:p-lg">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="font-h2 text-h2 text-on-surface">Oda Bazlı Saatlik İsraf Maliyeti (₺)</h2>
            <span className="material-symbols-outlined text-outline">more_horiz</span>
          </div>

          <div className="relative flex h-[250px] w-full items-end justify-between gap-2 px-2 pb-6">
            {rooms.map((room) => {
              const cost = room?.analysis?.financial?.wasted_cost_per_hour ?? 0;
              const maxCost = Math.max(...rooms.map((r) => r?.analysis?.financial?.wasted_cost_per_hour ?? 0), 1);
              const height = `${Math.round((cost / maxCost) * 100)}%`;
              return (
                <div key={room.room_id} className="flex w-full flex-col items-center gap-2">
                  <div className="group relative w-full rounded-t-lg bg-[#f97316]/30" style={{ height: height || '2%' }}>
                    <div className="absolute -top-8 left-1/2 -translate-x-1/2 rounded bg-inverse-surface px-2 py-1 text-xs text-inverse-on-surface opacity-0 transition-opacity group-hover:opacity-100">
                      ₺{cost.toFixed(2)}
                    </div>
                  </div>
                  <span className="font-caption text-caption text-outline">{room.room_id}</span>
                </div>
              );
            })}
            <div className="absolute bottom-6 left-0 w-full border-b border-surface-variant" />
          </div>
        </article>
      </section>

      {/* Anomaly Log Table */}
      <section className="rounded-[32px] border border-surface-container-highest bg-surface-container-lowest p-md shadow-[0_8px_30px_rgb(0,0,0,0.04)] lg:p-lg">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="font-h2 text-h2 text-on-surface">Oda Analiz Kayıtları</h2>
          <div className="flex gap-2">
            <button onClick={() => alert('Filtreleme seçenekleri açıldı')} className="rounded-lg p-2 text-outline transition-colors hover:bg-surface-container">
              <span className="material-symbols-outlined">filter_list</span>
            </button>
            <button onClick={() => alert('Arama alanı açıldı')} className="rounded-lg p-2 text-outline transition-colors hover:bg-surface-container">
              <span className="material-symbols-outlined">search</span>
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-left">
            <thead>
              <tr className="border-b border-surface-variant">
                <th className="px-4 py-4 font-label-sm text-label-sm font-medium text-on-surface-variant">Oda ID</th>
                <th className="px-4 py-4 font-label-sm text-label-sm font-medium text-on-surface-variant">Cihaz</th>
                <th className="px-4 py-4 font-label-sm text-label-sm font-medium text-on-surface-variant">İsraf Güç (kW)</th>
                <th className="px-4 py-4 font-label-sm text-label-sm font-medium text-on-surface-variant">Günlük Kayıp (₺)</th>
                <th className="px-4 py-4 font-label-sm text-label-sm font-medium text-on-surface-variant">Durum</th>
              </tr>
            </thead>
            <tbody className="font-body-md text-body-md text-on-surface">
              {anomalies.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-4 py-8 text-center text-on-surface-variant">
                    {loading ? 'Yükleniyor...' : 'Anomali tespit edilmedi — tüm odalar normal'}
                  </td>
                </tr>
              )}
              {anomalies.map((row, index) => (
                <tr
                  key={`${row.roomId}-${index}`}
                  className={[
                    index !== anomalies.length - 1 ? 'border-b border-surface-variant/50' : '',
                    'group transition-colors hover:bg-surface-container-lowest',
                  ].join(' ')}
                >
                  <td className="px-4 py-4 font-medium">{row.roomId}</td>
                  <td className="px-4 py-4 text-on-surface-variant">{row.device}</td>
                  <td className="px-4 py-4">{row.wastedPowerKw}</td>
                  <td className="px-4 py-4">₺{row.financialLossTl}</td>
                  <td className="px-4 py-4">
                    <span className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ${getStatusClass(row.status)}`}>
                      {row.status === 'CRITICAL' ? 'KRİTİK' : 
                       row.status === 'WARNING' ? 'UYARI' : 
                       row.status === 'ATTENTION' ? 'DİKKAT' : 
                       row.status === 'ANOMALY' ? 'ANOMALİ' : 
                       row.status === 'ACTIVE' ? 'AKTİF' : 
                       row.status === 'NORMAL' ? 'NORMAL' : row.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

function SummaryCard({ label, value, icon, color, bg }) {
  return (
    <div className={`flex items-center gap-4 rounded-2xl ${bg} p-5 border border-white/50`}>
      <div className={`flex h-11 w-11 items-center justify-center rounded-xl bg-white shadow-sm ${color}`}>
        <span className="material-symbols-outlined">{icon}</span>
      </div>
      <div>
        <p className="text-xs font-medium text-on-surface-variant">{label}</p>
        <p className="text-xl font-bold text-on-surface">{value}</p>
      </div>
    </div>
  );
}
