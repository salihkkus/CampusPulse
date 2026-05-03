import React, { useState, useEffect, useCallback } from 'react';
import { useApi } from '../hooks/useApi';
import { getFrontendRooms, getRangeReport } from '../services/api';
import TimeSelector from '../components/TimeSelector';
import DateRangeSelector from '../components/DateRangeSelector';

function getStatusClass(status) {
  if (status === 'CRITICAL') return 'bg-error-container text-on-error-container';
  if (status === 'WARNING' || status === 'ATTENTION') return 'bg-[#fef9c3] text-[#854d0e]';
  if (status === 'NORMAL' || status === 'ACTIVE') return 'bg-[#dcfce7] text-[#166534]';
  return 'bg-[#e0e7ff] text-[#3730a3]';
}

export default function ReportsPage() {
  const [selectedTime, setSelectedTime] = useState(null);
  const [isRangeMode, setIsRangeMode] = useState(false);
  const [rangeParams, setRangeParams] = useState({
    startDate: null,
    endDate: null,
    startHour: 0,
    endHour: 23
  });
  
  const selectedDate = selectedTime ? new Date(selectedTime).toISOString().split('T')[0] : null;

  // Single timestamp data
  const { data: batchData, loading: batchLoading } = useApi(
    () => !isRangeMode ? getFrontendRooms(selectedTime) : Promise.resolve(null), 
    [selectedTime, isRangeMode], 
    30_000
  );

  // Range report data
  const { data: rangeData, loading: rangeLoading } = useApi(
    () => (isRangeMode && rangeParams.startDate && rangeParams.endDate) 
      ? getRangeReport(rangeParams.startDate, rangeParams.endDate, rangeParams.startHour, rangeParams.endHour) 
      : Promise.resolve(null),
    [isRangeMode, rangeParams]
  );

  const loading = batchLoading || rangeLoading;
  
  const handleRangeChange = useCallback((newParams) => {
    setRangeParams(newParams);
  }, []);

  // Normalize data for UI
  const rooms = isRangeMode ? (rangeData?.rooms || []) : (batchData?.rooms || []);
  const summary = isRangeMode ? (rangeData?.summary || {}) : (batchData?.summary || {});

  // Build carbon data per room
  const carbonData = rooms.map((r) => ({
    label: r.room_id,
    value: isRangeMode ? (r.total_carbon_kg ?? 0) : (r.carbon_kg_per_hour ?? 0),
  }));

  const maxCarbon = Math.max(...carbonData.map((d) => d.value), 0.1);

  // Build anomaly log from rooms (only for single time mode as range is aggregate)
  const anomalies = !isRangeMode ? rooms
    .filter((r) => r.status !== 'NORMAL' && r.status !== 'ACTIVE')
    .map((r) => ({
      dateTime: r.timestamp,
      roomId: r.room_id,
      device: r.detected_device || '-',
      wastedPowerKw: ((r.current_power ?? 0) / 1000).toFixed(2),
      financialLossTl: (r.instant_loss_tl ?? 0).toFixed(2),
      status: r.status,
    })) : [];

  // Summary stats
  const totalWasteCost = isRangeMode ? (summary.total_waste_tl ?? 0) : (summary.total_waste_tl ?? 0);
  const totalPower = isRangeMode ? (summary.total_power_kwh ?? 0) : ((summary.total_power_watts ?? 0) / 1000);

  return (
    <div className="mx-auto flex w-full max-w-7xl flex-col gap-lg">
      {/* Header */}
      <section className="text-center">
        <h1 className="font-h1 text-h1 text-on-surface">Enerji &amp; Finansal Raporlar</h1>
        <p className="text-on-surface-variant font-body-md">
          {isRangeMode 
            ? `${rangeParams.startDate} - ${rangeParams.endDate} tarihleri arası kapsamlı analiz.` 
            : (selectedTime ? "Seçilen zaman dilimine ait detaylı rapor." : "Kampüs genel enerji ve finansal verimlilik raporları.")}
        </p>
      </section>

      {/* Kontrol Paneli */}
      <section className="glass-card flex flex-col gap-8 bg-white/50 p-8 backdrop-blur-sm">
        <div className="flex flex-col items-center justify-between gap-6 border-b border-surface-variant/30 pb-6 md:flex-row">
          <div className="flex items-center gap-4">
             <div className="flex items-center rounded-2xl bg-surface-container-low p-1.5 shadow-inner">
               <button 
                  onClick={() => setIsRangeMode(false)}
                  className={`rounded-xl px-4 py-2 text-sm font-bold transition-all ${!isRangeMode ? 'bg-primary text-white shadow-md' : 'text-on-surface-variant hover:bg-surface-variant/50'}`}
               >
                  Tekil Saat
               </button>
               <button 
                  onClick={() => setIsRangeMode(true)}
                  className={`rounded-xl px-4 py-2 text-sm font-bold transition-all ${isRangeMode ? 'bg-primary text-white shadow-md' : 'text-on-surface-variant hover:bg-surface-variant/50'}`}
               >
                  Tarih Aralığı
               </button>
             </div>
          </div>
          
          <div className="flex items-center gap-2 text-on-surface-variant">
             <span className="material-symbols-outlined text-primary/60">info</span>
             <span className="text-xs font-medium">
               {isRangeMode ? "Seçilen iki tarih arasındaki tüm veriler toplanarak analiz edilir." : "Seçilen ana ait anlık durum raporu oluşturulur."}
             </span>
          </div>
        </div>
        
        {isRangeMode ? (
          <DateRangeSelector onRangeChange={handleRangeChange} />
        ) : (
          <TimeSelector onTimeChange={setSelectedTime} selectedTime={selectedTime} />
        )}
      </section>

      {/* Action Bar */}
      <section className="flex justify-end gap-3">
        <button 
          onClick={() => {
            const params = new URLSearchParams({ startDate: rangeParams.startDate, endDate: rangeParams.endDate });
            window.open(`/api/v1/reports/export/pdf?${params.toString()}`, '_blank');
          }} 
          className="flex items-center gap-2 rounded-xl border border-surface-variant bg-surface-container-lowest px-4 py-2.5 font-label-sm text-label-sm text-on-surface-variant shadow-sm transition-all hover:-translate-y-px"
        >
          <span className="material-symbols-outlined text-[18px]">file_copy</span>
          PDF
        </button>
        <button 
          onClick={() => {
            const params = new URLSearchParams({ startDate: rangeParams.startDate, endDate: rangeParams.endDate });
            window.open(`/api/v1/reports/export/csv?${params.toString()}`, '_blank');
          }} 
          className="flex items-center gap-2 rounded-xl border border-surface-variant bg-surface-container-lowest px-4 py-2.5 font-label-sm text-label-sm text-on-surface-variant shadow-sm transition-all hover:-translate-y-px"
        >
          <span className="material-symbols-outlined text-[18px]">download</span>
          CSV
        </button>
      </section>

      {/* Live Summary Cards */}
      <section className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <SummaryCard
          label={isRangeMode ? "Analiz Edilen Oda" : "Toplam Oda"}
          value={isRangeMode ? (summary.analyzed_rooms ?? 0) : (summary.total_rooms ?? 0)}
          icon="meeting_room"
          color="text-indigo-600"
          bg="bg-indigo-50"
        />
        <SummaryCard
          label={isRangeMode ? "Toplam Tüketim" : "Anlık Tüketim"}
          value={`${totalPower.toFixed(1)} kWh`}
          icon="bolt"
          color="text-amber-600"
          bg="bg-amber-50"
        />
        <SummaryCard
          label={isRangeMode ? "Aralık İsrafı" : "Saatlik İsraf"}
          value={`₺${totalWasteCost.toFixed(2)}`}
          icon="payments"
          color="text-red-600"
          bg="bg-red-50"
        />
        <SummaryCard
          label={isRangeMode ? "Aralık Emisyonu" : "Saatlik Emisyon"}
          value={`${(isRangeMode ? (summary.total_carbon_kg ?? 0) : (summary.total_carbon_kg ?? 0)).toFixed(1)} kg`}
          icon="eco"
          color="text-emerald-600"
          bg="bg-emerald-50"
        />
      </section>

      {/* Charts Row */}
      <section className="grid grid-cols-1 gap-8 lg:grid-cols-2">
        {/* Main Energy Trend (Line Chart) */}
        <article className="flex flex-col rounded-[32px] border border-surface-container-highest bg-surface-container-lowest p-6 shadow-[0_8px_30px_rgb(0,0,0,0.04)] lg:p-8">
          <div className="mb-6">
            <h2 className="flex items-center gap-2 font-h2 text-h2 text-on-surface">
              <span className="material-symbols-outlined text-emerald-500">trending_up</span>
              {isRangeMode ? "Enerji Tüketim Trendi" : "Anlık Tüketim Analizi"}
            </h2>
            <p className="text-xs font-medium text-on-surface-variant/70">
              {isRangeMode ? "Seçili aralıktaki günlük kWh değişimi" : "Oda bazlı anlık güç dağılımı"}
            </p>
          </div>

          <div className="relative h-[400px] w-full flex flex-col">
            <div className="flex-1 flex w-full gap-4 overflow-hidden">
              {/* Y-Axis Labels */}
              <div className="flex h-full w-8 flex-col justify-between py-1 text-right text-[9px] font-bold text-on-surface-variant/40">
                {(() => {
                  const maxVal = Math.max(...rooms.map(rm => isRangeMode ? (rm.total_power_kwh ?? 0) : (rm.current_power ?? 0)), 1);
                  return [maxVal, maxVal * 0.75, maxVal * 0.5, maxVal * 0.25, 0].map((v, i) => (
                    <span key={i}>{v.toFixed(0)}</span>
                  ));
                })()}
              </div>

              {/* Chart Main Area */}
              <div className="relative flex-1 bg-surface-container-lowest/50 rounded-xl overflow-hidden">
                {loading ? (
                  <div className="flex h-full items-center justify-center animate-pulse text-on-surface-variant">Yükleniyor...</div>
                ) : (
                  <svg className="h-full w-full" viewBox="0 0 100 100" preserveAspectRatio="none">
                    <defs>
                      <linearGradient id="lineGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="rgba(16, 185, 129, 0.2)" />
                        <stop offset="100%" stopColor="rgba(16, 185, 129, 0)" />
                      </linearGradient>
                    </defs>
                    {/* Horizontal Grid Lines */}
                    {[0, 25, 50, 75, 100].map(v => (
                      <line key={v} x1="0" y1={v} x2="100" y2={v} stroke="currentColor" className="text-outline/10" strokeWidth="0.5" strokeDasharray="2,2" />
                    ))}
                    {/* The Path */}
                    {(() => {
                      const points = rooms.map((r, i) => {
                        const val = isRangeMode ? (r.total_power_kwh ?? 0) : (r.current_power ?? 0);
                        const maxVal = Math.max(...rooms.map(rm => isRangeMode ? (rm.total_power_kwh ?? 0) : (rm.current_power ?? 0)), 1);
                        const x = (i / Math.max(rooms.length - 1, 1)) * 100;
                        const y = 100 - (val / maxVal) * 80 - 10;
                        return `${x},${y}`;
                      }).join(' L ');
                      
                      if (!points) return null;
                      
                      return (
                        <>
                          <polyline
                            fill="none"
                            stroke="#10b981"
                            strokeWidth="2"
                            strokeLinecap="round"
                            points={points.replace(/ L /g, ' ')}
                            className="animate-draw-path"
                            style={{ filter: 'drop-shadow(0 4px 6px rgba(16, 185, 129, 0.2))' }}
                          />
                          <path
                            d={`M 0,100 L ${points} L 100,100 Z`}
                            fill="url(#lineGradient)"
                            className="opacity-50"
                          />
                        </>
                      );
                    })()}
                  </svg>
                )}
              </div>
            </div>
            
            {/* X-Axis Labels */}
            <div className="flex justify-between pl-12 pr-2 pt-2 text-[8px] font-bold text-on-surface-variant/50 uppercase tracking-tighter">
              {(() => {
                const count = 5;
                const labels = [];
                if (rooms.length > 0) {
                  const step = Math.max(Math.floor(rooms.length / (count - 1)), 1);
                  for (let i = 0; i < count; i++) {
                    const idx = Math.min(i * step, rooms.length - 1);
                    const r = rooms[idx];
                    labels.push(isRangeMode ? (r.room_id.split('_')[0]) : r.room_id);
                  }
                }
                return labels.map((l, i) => <span key={i} className="flex-1 text-center first:text-left last:text-right">{l}</span>);
              })()}
            </div>
          </div>
        </article>

        {/* Top Carbon Emitting Rooms (Horizontal Bar Chart) */}
        <article className="flex flex-col rounded-[32px] border border-surface-container-highest bg-surface-container-lowest p-6 shadow-[0_8px_30px_rgb(0,0,0,0.04)] lg:p-8">
          <div className="mb-6">
            <h2 className="flex items-center gap-2 font-h2 text-h2 text-on-surface">
              <span className="material-symbols-outlined text-teal-500">cloud_done</span>
              En Yüksek Karbon Salınımı
            </h2>
            <p className="text-xs font-medium text-on-surface-variant/70">En fazla emisyon üreten ilk 10 oda (kg CO₂)</p>
          </div>

          <div className="flex flex-1 flex-col gap-4 justify-center h-[400px]">
            {loading ? (
              <div className="flex h-full items-center justify-center animate-pulse text-on-surface-variant">Analiz ediliyor...</div>
            ) : (
              rooms.slice(0, 10).map((room, idx) => {
                const val = isRangeMode ? (room.total_carbon_kg ?? 0) : (room.carbon_kg_per_hour ?? 0);
                const maxVal = Math.max(...rooms.map(r => isRangeMode ? (r.total_carbon_kg ?? 0) : (r.carbon_kg_per_hour ?? 0)), 0.1);
                const w = (val / maxVal) * 100;
                return (
                  <div key={room.room_id} className="flex flex-col gap-1">
                    <div className="flex justify-between items-end">
                      <span className="text-[10px] font-bold text-on-surface uppercase tracking-tight">{room.room_name || room.room_id}</span>
                      <span className="text-[10px] font-black text-teal-600">{val.toFixed(2)} kg</span>
                    </div>
                    <div className="h-2 w-full overflow-hidden rounded-full bg-surface-container">
                      <div 
                        className="h-full rounded-full bg-gradient-to-r from-teal-500 to-emerald-400 transition-all duration-1000"
                        style={{ width: `${w}%`, transitionDelay: `${idx * 0.1}s` }}
                      />
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </article>

        {/* Building Distribution (Pie Chart) */}
        <article className="flex flex-col rounded-[32px] border border-surface-container-highest bg-surface-container-lowest p-6 shadow-[0_8px_30px_rgb(0,0,0,0.04)] lg:p-8">
          <div className="mb-8">
            <h2 className="flex items-center gap-2 font-h2 text-h2 text-on-surface">
              <span className="material-symbols-outlined text-indigo-500">pie_chart</span>
              Bina Bazlı Tüketim Payı
            </h2>
          </div>
          
          <div className="flex flex-1 flex-col items-center justify-center gap-8 sm:flex-row h-[400px]">
            <div className="relative h-48 w-48">
              <svg className="h-full w-full -rotate-90" viewBox="0 0 36 36">
                {(() => {
                  const buildingData = {};
                  rooms.forEach(r => {
                    const b = r.building || "Diğer";
                    buildingData[b] = (buildingData[b] || 0) + (isRangeMode ? (r.total_power_kwh ?? 0) : (r.current_power ?? 0));
                  });
                  const total = Object.values(buildingData).reduce((a, b) => a + b, 0) || 1;
                  const colors = ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ec4899'];
                  let offset = 0;
                  
                  return Object.entries(buildingData).map(([name, val], i) => {
                    const perc = (val / total) * 100;
                    const dash = `${perc} ${100 - perc}`;
                    const currentOffset = offset;
                    offset += perc;
                    return (
                      <circle
                        key={name}
                        cx="18" cy="18" r="16"
                        fill="none"
                        stroke={colors[i % colors.length]}
                        strokeWidth="3.5"
                        strokeDasharray={dash}
                        strokeDashoffset={-currentOffset}
                        className="transition-all duration-1000"
                        style={{ filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))' }}
                      />
                    );
                  });
                })()}
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-2xl font-black text-on-surface">%{((summary.total_power_kwh || 0) > 0 ? 100 : 0)}</span>
                <span className="text-[10px] font-bold text-on-surface-variant uppercase">Kapsam</span>
              </div>
            </div>

            <div className="flex flex-col gap-3">
              {(() => {
                  const buildingData = {};
                  rooms.forEach(r => {
                    const b = r.building || "Diğer";
                    buildingData[b] = (buildingData[b] || 0) + (isRangeMode ? (r.total_power_kwh ?? 0) : (r.current_power ?? 0));
                  });
                  const total = Object.values(buildingData).reduce((a, b) => a + b, 0) || 1;
                  const colors = ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ec4899'];
                  
                  return Object.entries(buildingData).map(([name, val], i) => (
                    <div key={name} className="flex items-center gap-3">
                      <div className="h-3 w-3 rounded-full" style={{ backgroundColor: colors[i % colors.length] }} />
                      <div className="flex flex-col">
                        <span className="text-xs font-bold text-on-surface">{name}</span>
                        <span className="text-[10px] text-on-surface-variant">%{((val / total) * 100).toFixed(1)}</span>
                      </div>
                    </div>
                  ));
              })()}
            </div>
          </div>
        </article>

        {/* Room Type Distribution */}
        <article className="flex flex-col rounded-[32px] border border-surface-container-highest bg-surface-container-lowest p-6 shadow-[0_8px_30px_rgb(0,0,0,0.04)] lg:p-8">
          <div className="mb-8">
            <h2 className="flex items-center gap-2 font-h2 text-h2 text-on-surface">
              <span className="material-symbols-outlined text-purple-500">category</span>
              Kategori Analizi
            </h2>
          </div>
          
          <div className="flex flex-1 flex-col gap-6 justify-center h-[400px]">
            {(() => {
              const typeData = {};
              rooms.forEach(r => {
                const parts = r.room_id.split('_');
                const t = parts[1] || "Diğer";
                typeData[t] = (typeData[t] || 0) + (isRangeMode ? (r.total_power_kwh ?? 0) : (r.current_power ?? 0));
              });
              const maxVal = Math.max(...Object.values(typeData), 1);
              
              return Object.entries(typeData).map(([name, val]) => (
                <div key={name} className="flex flex-col gap-1.5">
                  <div className="flex justify-between text-xs font-bold">
                    <span className="text-on-surface">{name}</span>
                    <span className="text-on-surface-variant">{val.toFixed(1)} kWh</span>
                  </div>
                  <div className="h-3 w-full overflow-hidden rounded-full bg-surface-container">
                    <div 
                      className="h-full rounded-full bg-purple-500 transition-all duration-1000"
                      style={{ width: `${(val / maxVal) * 100}%` }}
                    />
                  </div>
                </div>
              ));
            })()}
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
