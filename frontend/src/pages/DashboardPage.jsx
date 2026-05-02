import React from 'react';
import MetricCard from '../components/MetricCard';
import DeviceCostPieChart from '../components/charts/DeviceCostPieChart';
import ThreeDMap from '../components/ThreeDMap';
import RoomStatusCard from '../components/RoomStatusCard';
import { useApi } from '../hooks/useApi';
import { getDashboardSummary, getBatchAnalysis, getFrontendAlerts } from '../services/api';
import { getDeviceCostBreakdownChart, dashboardAlerts as fallbackAlerts } from '../data/mockData';

export default function DashboardPage() {
  // Live data from backend – auto-refresh every 30s
  const { data: dashData, loading: dashLoading } = useApi(getDashboardSummary, [], 30_000);
  const { data: batchData, loading: batchLoading } = useApi(getBatchAnalysis, [], 30_000);
  const { data: alertsData } = useApi(getFrontendAlerts, [], 30_000);

  // Extract values safely
  const summary = dashData?.data?.summary;
  const rooms = batchData?.data?.rooms || [];
  const liveAlerts = alertsData?.alerts || [];

  // Metric values (live or fallback)
  const totalWastePerHour = summary?.total_waste_per_hour ?? 0;
  const dailyCost = totalWastePerHour * 24;
  const totalRooms = summary?.total_rooms ?? 0;
  const wastingRooms = summary?.wasting_rooms ?? 0;
  const criticalRooms = summary?.critical_rooms ?? 0;

  // Carbon estimate from rooms
  const totalCarbon = rooms.reduce(
    (sum, r) => sum + (r?.analysis?.financial?.instant_carbon_per_hour ?? 0),
    0
  );

  // Device cost breakdown from live rooms
  const deviceBreakdown = buildDeviceBreakdown(rooms);
  const chartData =
    deviceBreakdown.length > 0 ? deviceBreakdown : getDeviceCostBreakdownChart();

  // Alerts: prefer live, fallback to mock
  const alerts =
    liveAlerts.length > 0
      ? liveAlerts.map((a) => ({
          title: a.message || a.title || 'Alert',
          label: a.room_id,
          location: a.room_id,
          severity: a.severity === 'critical' ? 'Critical' : a.severity === 'high' ? 'High' : 'Normal',
          time: 'Now',
          icon: a.severity === 'critical' ? 'warning' : a.severity === 'high' ? 'lightbulb' : 'info',
          tone: a.severity === 'critical' ? 'error' : a.severity === 'high' ? 'amber' : 'blue',
        }))
      : fallbackAlerts;

  const isLoading = dashLoading || batchLoading;

  return (
    <>
      {/* ── Connection Status ────────────────────────── */}
      {!isLoading && summary && (
        <div className="flex items-center gap-2 rounded-xl bg-emerald-50 px-4 py-2 text-sm text-emerald-700 mb-2">
          <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          Backend bagli — {totalRooms} oda izleniyor
        </div>
      )}
      {!isLoading && !summary && (
        <div className="flex items-center gap-2 rounded-xl bg-amber-50 px-4 py-2 text-sm text-amber-700 mb-2">
          <span className="material-symbols-outlined text-[16px]">cloud_off</span>
          Backend baglantisi kurulamadi — mock veri gosteriliyor
        </div>
      )}

      {/* ── Top Metric Cards ─────────────────────────── */}
      <section className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          title="Instant Loss (Hourly)"
          value={`₺${totalWastePerHour.toFixed(2)}`}
          subtext={`${wastingRooms} oda israf yapiyor`}
          icon="trending_down"
          iconTone="text-error"
          gradientClass="from-red-50 to-orange-100"
        />
        <MetricCard
          title="Estimated Daily Cost"
          value={`₺${dailyCost.toFixed(2)}`}
          subtext="Based on current consumption"
          icon="payments"
          iconTone="text-orange-500"
          gradientClass="from-yellow-50 to-orange-100/50"
        />
        <MetricCard
          title="Carbon Footprint (Hourly)"
          value={totalCarbon.toFixed(2)}
          valueSuffix=" kg CO₂"
          subtext="Total campus emissions"
          icon="eco"
          iconTone="text-emerald-500"
          gradientClass="from-emerald-50 to-green-100"
        />
        <MetricCard
          title="Rooms Overview"
          value={`${criticalRooms}`}
          valueSuffix={` / ${totalRooms}`}
          subtext="Critical / Total rooms"
          icon="meeting_room"
          iconTone="text-primary"
          gradientClass="from-indigo-50 to-violet-100/50"
        />
      </section>

      {/* ── Alerts + Pie Chart ───────────────────────── */}
      <section className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="glass-card flex flex-col p-6 lg:col-span-2">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="font-h2 text-h2 text-on-surface">Latest Anomalies / Alerts</h2>
            <span className="flex items-center gap-1 rounded-full bg-error-container/40 px-3 py-1 text-xs font-medium text-on-error-container">
              {alerts.length} alert{alerts.length !== 1 ? 's' : ''}
            </span>
          </div>

          <div className="flex flex-1 flex-col gap-3">
            {alerts.length === 0 && (
              <p className="py-8 text-center text-on-surface-variant">No active alerts</p>
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
                    <span className="rounded-full bg-secondary-container px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider text-on-secondary-container">
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

        <div className="glass-card flex flex-col p-6">
          <h2 className="mb-4 font-h2 text-h2 text-on-surface">Cost Breakdown by Device</h2>
          <div className="min-h-[220px] flex-1 w-full">
            <DeviceCostPieChart data={chartData} />
          </div>
          <div className="mt-4 border-t border-surface-container pt-4">
            <button className="flex w-full items-center justify-center gap-2 rounded-xl bg-surface-container px-4 py-3 text-sm font-medium text-on-surface transition-colors hover:bg-surface-variant">
              <span className="material-symbols-outlined text-[18px]">download</span>
              Download Full Report
            </button>
          </div>
        </div>
      </section>

      {/* ── Room Status Cards ────────────────────────── */}
      {rooms.length > 0 && (
        <section>
          <h2 className="mb-4 font-h2 text-h2 text-on-surface">Room Status (Live)</h2>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
            {rooms.map((room) => (
              <RoomStatusCard key={room.room_id} room={room} />
            ))}
          </div>
        </section>
      )}

      {/* ── 3D Map ───────────────────────────────────── */}
      <section className="glass-card flex flex-col p-6">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h2 className="font-h2 text-h2 text-on-surface">Live 3D Digital Twin</h2>
            <p className="mt-1 font-caption text-caption text-on-surface-variant">
              Real-time thermal and energy mapping
            </p>
          </div>
          <span className="flex items-center gap-1 rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-600">
            <span className="h-2 w-2 rounded-full bg-red-500 animate-pulse" />
            High Consumption
          </span>
        </div>
        <div className="relative flex min-h-[400px] flex-col items-center justify-center overflow-hidden rounded-2xl border border-surface-variant bg-surface-container-low">
          <ThreeDMap />
        </div>
      </section>
    </>
  );
}

/* ── helpers ──────────────────────────────────────────────── */
const deviceLabels = {
  klima: 'Klima',
  aydinlatma: 'Aydinlatma',
  projeksiyon: 'Projeksiyon',
  pc_20_adet: "PC'ler (20)",
  pc: 'PC',
  server: 'Server',
  fiyans: 'Fiyans',
  buzdolabi: 'Buzdolabi',
  su_isitici: 'Su Isitici',
  laboratuvar: 'Laboratuvar',
};

const deviceColors = {
  klima: '#FFADAD',
  aydinlatma: '#CAFFBF',
  projeksiyon: '#9BF6FF',
  pc_20_adet: '#BDB2FF',
  pc: '#FFC6FF',
  server: '#FDFFB6',
  fiyans: '#A0C4FF',
  buzdolabi: '#FFD6A5',
  su_isitici: '#FF9B9B',
  laboratuvar: '#C5DFF8',
};

function buildDeviceBreakdown(rooms) {
  const totals = {};
  for (const room of rooms) {
    const devices = room?.current_data?.detected_devices || [];
    const costPerDevice =
      (room?.analysis?.financial?.instant_loss_per_hour ?? 0) / (devices.length || 1);
    const carbonPerDevice =
      (room?.analysis?.financial?.instant_carbon_per_hour ?? 0) / (devices.length || 1);

    for (const d of devices) {
      if (!totals[d]) totals[d] = { cost: 0, carbon: 0 };
      totals[d].cost += costPerDevice;
      totals[d].carbon += carbonPerDevice;
    }
  }
  return Object.entries(totals).map(([key, v]) => ({
    key,
    name: deviceLabels[key] ?? key,
    value: parseFloat(v.cost.toFixed(2)),
    carbon: parseFloat(v.carbon.toFixed(3)),
    section: 'Equipment',
    color: deviceColors[key] ?? '#6B7280',
  }));
}
