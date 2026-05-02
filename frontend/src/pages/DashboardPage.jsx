import React from 'react';
import MetricCard from '../components/MetricCard';
import DeviceCostPieChart from '../components/charts/DeviceCostPieChart';
import ThreeDMap from '../components/ThreeDMap';
import { apiResponseData, dashboardAlerts, getDeviceCostBreakdownChart } from '../data/mockData';

export default function DashboardPage() {
  const chartData = getDeviceCostBreakdownChart();

  return (
    <>
      <section className="grid grid-cols-1 gap-6 md:grid-cols-3">
        <MetricCard
          title="Instant Loss (Hourly)"
          value={`₺${apiResponseData.instant_loss_tl_per_hour.toFixed(2)}`}
          subtext="Real-time leakage detected"
          icon="trending_down"
          iconTone="text-error"
          gradientClass="from-red-50 to-orange-100"
        />
        <MetricCard
          title="Estimated Daily Cost"
          value={`₺${apiResponseData.daily_cost_tl.toFixed(2)}`}
          subtext="Based on current consumption"
          icon="payments"
          iconTone="text-orange-500"
          gradientClass="from-yellow-50 to-orange-100/50"
        />
        <MetricCard
          title="Carbon Footprint (Hourly)"
          value={apiResponseData.carbon_kg_per_hour.toFixed(2)}
          valueSuffix=" kg CO2"
          subtext="Sustainability Index: Good"
          icon="eco"
          iconTone="text-emerald-500"
          gradientClass="from-emerald-50 to-green-100"
        />
      </section>

      <section className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="glass-card flex flex-col p-6 lg:col-span-2">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="font-h2 text-h2 text-on-surface">Latest Anomalies / Alerts</h2>
            <button className="text-sm font-medium text-primary transition-colors hover:text-surface-tint">View All</button>
          </div>

          <div className="flex flex-1 flex-col gap-3">
            {dashboardAlerts.map((alert) => (
              <div
                key={alert.title}
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

      <section className="glass-card flex flex-col p-6">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h2 className="font-h2 text-h2 text-on-surface">Live 3D Digital Twin</h2>
            <p className="mt-1 font-caption text-caption text-on-surface-variant">Real-time thermal and energy mapping</p>
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
