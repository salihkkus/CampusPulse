import React from 'react';
import { useNavigate } from 'react-router-dom';
import MetricCard from '../components/MetricCard';
import CampusMapViewer from '../components/CampusMapViewer';
import { useApi } from '../hooks/useApi';
import { getFrontendSummary, getFrontendRooms, getFrontendAlerts, getAvailableTimestamps, getBatchAnalysis } from '../services/api';
import { dashboardAlerts as fallbackAlerts } from '../data/mockData';
import TimeSelector from '../components/TimeSelector';

export default function DashboardPage() {
  const navigate = useNavigate();
  const [selectedTime, setSelectedTime] = React.useState(null);

  // Mevcut zaman damgalarını al ve en sonuncuyu seç
  React.useEffect(() => {
    let cancelled = false;
    getAvailableTimestamps().then(res => {
      if (cancelled) return;
      if (res.timestamps && res.timestamps.length > 0) {
        setSelectedTime(res.timestamps[res.timestamps.length - 1]);
      }
    }).catch(() => {});
    return () => { cancelled = true; };
  }, []);

  // Canlı veriler - seçilen zamana göre veya her 30 saniyede bir güncellenir
  const { data: dashData, loading: dashLoading } = useApi(() => getFrontendSummary(selectedTime), [selectedTime], 30_000);
  const { data: roomsData, loading: roomsLoading } = useApi(() => getFrontendRooms(selectedTime), [selectedTime], 30_000);
  const { data: alertsData } = useApi(() => getFrontendAlerts(selectedTime), [selectedTime], 30_000);

  // 3D Harita için batch-analysis (LiveMap ile aynı zengin veri)
  const { data: batchData, loading: batchLoading } = useApi(() => getBatchAnalysis(selectedTime), [selectedTime], 30_000);
  const batchRooms = batchData?.data?.rooms || [];

  // Verileri güvenli şekilde çıkar
  const summary = dashData?.overview;
  const rooms = roomsData?.rooms || [];
  const liveAlerts = alertsData?.alerts || [];

  // Metrik değerler
  const totalWastePerHour = summary?.total_waste_tl ?? 0;
  const projectedDailyCost = dashData?.financial_impact?.projected_daily_loss ?? (totalWastePerHour * 24);
  const totalRooms = summary?.total_rooms ?? 0;
  const criticalRoomsCount = (summary?.critical_rooms ?? 0) + (summary?.warning_rooms ?? 0);
  const totalCarbon = summary?.total_carbon_kg ?? 0;
  const totalPowerKwh = (summary?.total_power_watts ?? 0) / 1000;

  // Uyarılar
  const alerts = liveAlerts.map((a) => ({
    title: a.message || a.title || 'Uyarı',
    label: a.room_id,
    location: a.room_id,
    severity: a.severity === 'critical' ? 'Kritik' : a.severity === 'high' ? 'Yüksek' : 'Normal',
    time: 'Şimdi',
    icon: a.severity === 'critical' ? 'warning' : a.severity === 'high' ? 'lightbulb' : 'info',
    tone: a.severity === 'critical' ? 'error' : a.severity === 'high' ? 'amber' : 'blue',
  }));

  const isLoading = dashLoading || roomsLoading;

  return (
    <div className="flex flex-col gap-8">
      {/* ── Üst Başlık ────────────────────── */}
      <section className="text-center">
        <h1 className="font-h1 text-h1 text-on-surface">Kampüs Enerji Analizi</h1>
        <p className="text-on-surface-variant font-body-md">
          Gerçek zamanlı kampüs enerji tüketimi ve israf analizi.
        </p>
      </section>

      {/* ── Bağlantı Durumu ────────────────────────── */}
      {!isLoading && summary && (
        <div className="flex items-center gap-2 rounded-xl bg-emerald-50 px-4 py-2 text-sm text-emerald-700">
          <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          Veri kaynağı aktif — {totalRooms} oda izleniyor
        </div>
      )}
      {!isLoading && !summary && (
        <div className="flex items-center gap-2 rounded-xl bg-amber-50 px-4 py-2 text-sm text-amber-700">
          <span className="material-symbols-outlined text-[16px]">cloud_off</span>
          Veri yüklenemedi — örnek veri gösteriliyor
        </div>
      )}

      {/* ── Üst Metrik Kartları ─────────────────────────── */}
      <section className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-5">
        <MetricCard
          title="Anlık Kayıp (Saatlik)"
          value={`₺${totalWastePerHour.toFixed(2)}`}
          subtext="Seçilen saatteki toplam israf"
          icon="trending_down"
          iconTone="text-error"
          gradientClass="from-red-50 to-orange-100"
        />
        <MetricCard
          title="Tahmini Günlük Maliyet"
          value={`₺${projectedDailyCost.toFixed(2)}`}
          subtext="Mevcut tüketime göre"
          icon="payments"
          iconTone="text-orange-500"
          gradientClass="from-yellow-50 to-orange-100/50"
        />
        <MetricCard
          title="Karbon Ayak İzi (Saatlik)"
          value={totalCarbon.toFixed(2)}
          valueSuffix=" kg CO₂"
          subtext="Kampüs toplam emisyonu"
          icon="eco"
          iconTone="text-emerald-500"
          gradientClass="from-emerald-50 to-green-100"
        />
        <MetricCard
          title="Toplam Güç Tüketimi"
          value={totalPowerKwh.toFixed(1)}
          valueSuffix=" kWh"
          subtext="Anlık kampüs toplamı"
          icon="bolt"
          iconTone="text-amber-500"
          gradientClass="from-amber-50 to-yellow-100"
        />
        <MetricCard
          title="Odalar Özeti"
          value={`${criticalRoomsCount}`}
          valueSuffix={` / ${totalRooms}`}
          subtext="Kritik / Toplam oda"
          icon="meeting_room"
          iconTone="text-primary"
          gradientClass="from-indigo-50 to-violet-100/50"
        />
      </section>

      {/* ── Uyarılar ───────────────────────── */}
      <section className="flex flex-col gap-6">
        <div className="glass-card flex flex-col p-6">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="font-h2 text-h2 text-on-surface">En Son Anomaliler / Uyarılar</h2>
            <span className="flex items-center gap-1 rounded-full bg-error-container/40 px-3 py-1 text-xs font-medium text-on-error-container">
              {alerts.length} uyarı
            </span>
          </div>

          <div className="flex flex-1 flex-col gap-3">
            {alerts.length === 0 && (
              <p className="py-8 text-center text-on-surface-variant">Aktif uyarı yok</p>
            )}
            {alerts.map((alert, idx) => (
              <div
                key={`${alert.title}-${idx}`}
                className="group flex cursor-pointer items-center gap-4 rounded-2xl border border-surface-container bg-surface-container-lowest p-4 transition-colors hover:bg-surface-container-low"
              >
                <div
                  className={`flex h-10 w-10 items-center justify-center rounded-full transition-colors ${
                    alert.tone === 'error'
                      ? 'bg-error-container/30 text-error group-hover:bg-error-container'
                      : alert.tone === 'amber'
                        ? 'bg-orange-100 text-orange-600 group-hover:bg-orange-200'
                        : 'bg-blue-100 text-blue-600 group-hover:bg-blue-200'
                  }`}
                >
                  <span className="material-symbols-outlined">{alert.icon}</span>
                </div>
                <div className="min-w-0 flex-1">
                  <h3 className="text-label-sm font-label-sm text-on-surface">{alert.title}</h3>
                  <div className="mt-1 flex items-center gap-2">
                    <span className="rounded-full bg-secondary-container px-2 py-0.5 text-[10px] font-bold tracking-wider text-on-secondary-container">
                      {alert.label}
                    </span>
                    <p className="flex items-center gap-1 font-caption text-caption text-on-surface-variant">
                      <span className="material-symbols-outlined text-[14px]">location_on</span>
                      {alert.location}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-label-sm font-label-sm text-error">{alert.severity}</p>
                  <p className="font-caption text-caption text-on-surface-variant">{alert.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Oda Durumları Bağlantısı ─────────────────────────── */}
      <section className="glass-card flex items-center justify-between p-6">
        <div>
          <h2 className="font-h2 text-h2 text-on-surface">Oda Durumları (Canlı)</h2>
          <p className="mt-1 font-caption text-caption text-on-surface-variant">
            {rooms.length} izlenen oda için detaylı gerçek zamanlı metrikler.
          </p>
        </div>
        <button
          onClick={() => navigate('/rooms')}
          className="flex items-center gap-2 rounded-xl bg-primary px-5 py-3 font-label-sm text-label-sm text-on-primary shadow-sm hover:bg-primary/90 transition-all"
        >
          Tüm Odaları Gör
          <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
        </button>
      </section>

      {/* ── 3D Harita ───────────────────────────────────── */}
      <CampusMapViewer
        rooms={batchRooms}
        loading={batchLoading}
        minHeight="400px"
        maxPanelH="600px"
      />
    </div>
  );
}
