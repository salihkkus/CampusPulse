import React, { useState } from 'react';

const statusConfig = {
  CRITICAL: { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-700', badge: 'bg-red-100 text-red-700', icon: 'error' },
  WARNING:  { bg: 'bg-amber-50', border: 'border-amber-200', text: 'text-amber-700', badge: 'bg-amber-100 text-amber-700', icon: 'warning' },
  ATTENTION:{ bg: 'bg-orange-50', border: 'border-orange-200', text: 'text-orange-700', badge: 'bg-orange-100 text-orange-700', icon: 'info' },
  ANOMALY:  { bg: 'bg-purple-50', border: 'border-purple-200', text: 'text-purple-700', badge: 'bg-purple-100 text-purple-700', icon: 'psychology' },
  ACTIVE:   { bg: 'bg-blue-50', border: 'border-blue-200', text: 'text-blue-700', badge: 'bg-blue-100 text-blue-700', icon: 'bolt' },
  NORMAL:   { bg: 'bg-emerald-50', border: 'border-emerald-200', text: 'text-emerald-700', badge: 'bg-emerald-100 text-emerald-700', icon: 'check_circle' },
};

export default function RoomStatusCard({ room }) {
  const [expanded, setExpanded] = useState(false);
  const status = room?.status ?? 'NORMAL';
  const cfg = statusConfig[status] || statusConfig.NORMAL;

  const analysis = room?.analysis || {};
  const diagnosis = analysis.diagnosis || {};
  const financial = analysis.financial || {};
  const currentData = room?.current_data || {};
  const recommendations = room?.recommendations || [];

  const power = currentData.power_consumption ?? 0;
  const occupancy = currentData.occupancy_status ?? 0;
  const devices = currentData.detected_devices || [];
  const costPerHour = financial.wasted_cost_per_hour ?? 0;
  const dailyCost = financial.daily_cost ?? 0;
  const carbonHour = financial.instant_carbon_per_hour ?? 0;
  const isWasting = diagnosis.is_wasting ?? false;
  const primaryIssue = diagnosis.primary_issue;

  return (
    <div
      className={`rounded-2xl border p-5 transition-all duration-200 cursor-pointer
        ${cfg.bg} ${cfg.border} hover:shadow-md`}
      onClick={() => setExpanded(!expanded)}
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className={`flex h-9 w-9 items-center justify-center rounded-xl ${cfg.badge}`}>
            <span className="material-symbols-outlined text-[20px]">{cfg.icon}</span>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-on-surface">{room.room_id}</h3>
            <p className="text-xs text-on-surface-variant">
              {occupancy ? 'Dolu' : 'Boş'} — {power.toFixed(0)}W
            </p>
          </div>
        </div>
        <span className={`rounded-full px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider ${cfg.badge}`}>
          {status === 'CRITICAL' ? 'KRİTİK' : 
           status === 'WARNING' ? 'UYARI' : 
           status === 'ATTENTION' ? 'DİKKAT' : 
           status === 'ANOMALY' ? 'ANOMALİ' : 
           status === 'ACTIVE' ? 'AKTİF' : 
           status === 'NORMAL' ? 'NORMAL' : status}
        </span>
      </div>

      {/* Quick stats */}
      {isWasting && (
        <div className="mt-3 flex items-center gap-4 text-xs">
          <span className="flex items-center gap-1 text-red-600">
            <span className="material-symbols-outlined text-[14px]">payments</span>
            ₺{costPerHour.toFixed(2)}/saat
          </span>
          <span className="flex items-center gap-1 text-orange-600">
            <span className="material-symbols-outlined text-[14px]">calendar_today</span>
            ₺{dailyCost.toFixed(2)}/gün
          </span>
          <span className="flex items-center gap-1 text-emerald-600">
            <span className="material-symbols-outlined text-[14px]">eco</span>
            {carbonHour.toFixed(2)} kg CO₂
          </span>
        </div>
      )}

      {/* Primary issue */}
      {primaryIssue && (
        <p className="mt-2 text-xs font-medium text-on-surface-variant">
          <span className="material-symbols-outlined align-middle text-[14px] mr-1">
            diagnosis
          </span>
          {primaryIssue}
        </p>
      )}

      {/* Devices */}
      {devices.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-1.5">
          {devices.map((d) => (
            <span
              key={d}
              className="rounded-full bg-white/70 px-2 py-0.5 text-[10px] font-medium text-on-surface-variant border border-white"
            >
              {d}
            </span>
          ))}
        </div>
      )}

      {/* Expanded details */}
      {expanded && recommendations.length > 0 && (
        <div className="mt-3 border-t border-white/50 pt-3 space-y-2">
          <p className="text-[10px] font-bold uppercase tracking-wider text-on-surface-variant">
            Öneriler
          </p>
          {recommendations.map((rec, i) => (
            <div key={i} className="flex items-start gap-2 text-xs text-on-surface-variant">
              <span className="material-symbols-outlined text-[14px] mt-0.5 text-primary">
                lightbulb
              </span>
              <span>{rec.title}: {rec.description}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
