import React from 'react';

const carbonWeekly = [
  { day: 'Mon', value: 120 },
  { day: 'Tue', value: 180 },
  { day: 'Wed', value: 150 },
  { day: 'Thu', value: 270 },
  { day: 'Fri', value: 210 },
  { day: 'Sat', value: 90 },
  { day: 'Sun', value: 60 },
];

const anomalies = [
  {
    dateTime: '2023-10-24 14:20',
    roomId: 'Lab-101',
    device: 'HVAC',
    wastedPowerKw: '1.2',
    financialLossTl: '15.50',
    status: 'Critical',
  },
  {
    dateTime: '2023-10-24 09:15',
    roomId: 'Hall-B',
    device: 'Lighting',
    wastedPowerKw: '0.5',
    financialLossTl: '5.20',
    status: 'Resolved',
  },
  {
    dateTime: '2023-10-23 22:45',
    roomId: 'Lib-Floor2',
    device: 'AC Unit',
    wastedPowerKw: '2.8',
    financialLossTl: '32.10',
    status: 'Ignored',
  },
  {
    dateTime: '2023-10-23 18:30',
    roomId: 'Cafeteria',
    device: 'Fridge',
    wastedPowerKw: '0.9',
    financialLossTl: '11.00',
    status: 'Resolved',
  },
  {
    dateTime: '2023-10-22 03:10',
    roomId: 'Dorm-A',
    device: 'Heating',
    wastedPowerKw: '3.5',
    financialLossTl: '45.00',
    status: 'Critical',
  },
];

function getStatusClass(status) {
  if (status === 'Critical') {
    return 'bg-error-container text-on-error-container';
  }

  if (status === 'Resolved') {
    return 'bg-[#dcfce7] text-[#166534]';
  }

  return 'bg-[#fef9c3] text-[#854d0e]';
}

export default function ReportsPage() {
  return (
    <div className="mx-auto flex w-full max-w-7xl flex-col gap-lg">
      <section className="mb-2 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
        <h1 className="font-h1 text-h1 text-on-surface">Energy &amp; Financial Reports</h1>

        <div className="flex flex-wrap items-center gap-3">
          <button className="flex items-center gap-2 rounded-xl border border-surface-variant bg-surface-container-lowest px-4 py-2.5 font-label-sm text-label-sm text-on-surface-variant shadow-[0_2px_10px_-2px_rgba(0,0,0,0.02)] transition-all hover:-translate-y-px hover:shadow-[0_4px_12px_-2px_rgba(0,0,0,0.05)]">
            <span className="material-symbols-outlined text-[18px]">calendar_today</span>
            Oct 18 - Oct 24
          </button>

          <button className="flex items-center gap-2 rounded-xl border border-surface-variant bg-surface-container-lowest px-4 py-2.5 font-label-sm text-label-sm text-on-surface-variant shadow-[0_2px_10px_-2px_rgba(0,0,0,0.02)] transition-all hover:-translate-y-px hover:shadow-[0_4px_12px_-2px_rgba(0,0,0,0.05)]">
            <span className="material-symbols-outlined text-[18px]">file_copy</span>
            Export PDF
          </button>

          <button className="flex items-center gap-2 rounded-xl border border-surface-variant bg-surface-container-lowest px-4 py-2.5 font-label-sm text-label-sm text-on-surface-variant shadow-[0_2px_10px_-2px_rgba(0,0,0,0.02)] transition-all hover:-translate-y-px hover:shadow-[0_4px_12px_-2px_rgba(0,0,0,0.05)]">
            <span className="material-symbols-outlined text-[18px]">download</span>
            Download CSV
          </button>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-lg lg:grid-cols-2">
        <article className="rounded-[32px] border border-surface-container-highest bg-surface-container-lowest p-md shadow-[0_8px_30px_rgb(0,0,0,0.04)] transition-all duration-300 hover:-translate-y-[2px] hover:shadow-[0_12px_40px_rgb(0,0,0,0.06)] lg:p-lg">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="font-h2 text-h2 text-on-surface">Weekly Carbon Footprint (kg CO2)</h2>
            <span className="material-symbols-outlined text-outline">more_horiz</span>
          </div>

          <div className="relative flex h-[250px] w-full items-end justify-between gap-2 px-2 pb-6">
            {carbonWeekly.map((item) => {
              const height = `${Math.round((item.value / 300) * 100)}%`;

              return (
                <div key={item.day} className="flex w-full flex-col items-center gap-2">
                  <div className="group relative w-full rounded-t-lg bg-[#10b981]/30" style={{ height }}>
                    <div className="absolute -top-8 left-1/2 -translate-x-1/2 rounded bg-inverse-surface px-2 py-1 text-xs text-inverse-on-surface opacity-0 transition-opacity group-hover:opacity-100">
                      {item.value}
                    </div>
                  </div>
                  <span className="font-caption text-caption text-outline">{item.day}</span>
                </div>
              );
            })}

            <div className="absolute bottom-6 left-0 w-full border-b border-surface-variant" />
            <div className="absolute bottom-[calc(6px+25%)] left-0 w-full border-b border-dashed border-surface-variant" />
            <div className="absolute bottom-[calc(6px+50%)] left-0 w-full border-b border-dashed border-surface-variant" />
            <div className="absolute bottom-[calc(6px+75%)] left-0 w-full border-b border-dashed border-surface-variant" />
          </div>
        </article>

        <article className="rounded-[32px] border border-surface-container-highest bg-surface-container-lowest p-md shadow-[0_8px_30px_rgb(0,0,0,0.04)] transition-all duration-300 hover:-translate-y-[2px] hover:shadow-[0_12px_40px_rgb(0,0,0,0.06)] lg:p-lg">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="font-h2 text-h2 text-on-surface">Weekly Wasted Cost (₺)</h2>
            <span className="material-symbols-outlined text-outline">more_horiz</span>
          </div>

          <div className="relative h-[250px] w-full px-4 pb-8 pt-4">
            <svg className="h-full w-full overflow-visible" viewBox="0 0 100 100" preserveAspectRatio="none">
              <defs>
                <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#f97316" />
                  <stop offset="100%" stopColor="#ef4444" />
                </linearGradient>
                <linearGradient id="areaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stopColor="#f97316" stopOpacity="0.2" />
                  <stop offset="100%" stopColor="#ef4444" stopOpacity="0" />
                </linearGradient>
              </defs>

              <path d="M0,80 Q16,60 33,70 T66,30 T100,50 L100,100 L0,100 Z" fill="url(#areaGrad)" />
              <path d="M0,80 Q16,60 33,70 T66,30 T100,50" fill="none" stroke="url(#lineGrad)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />

              <circle cx="0" cy="80" r="2" fill="white" stroke="#f97316" strokeWidth="1" />
              <circle cx="16" cy="65" r="2" fill="white" stroke="#f97316" strokeWidth="1" />
              <circle cx="33" cy="70" r="2" fill="white" stroke="#f97316" strokeWidth="1" />
              <circle cx="50" cy="50" r="2" fill="white" stroke="#ef4444" strokeWidth="1" />
              <circle cx="66" cy="30" r="2" fill="white" stroke="#ef4444" strokeWidth="1" />
              <circle cx="83" cy="40" r="2" fill="white" stroke="#ef4444" strokeWidth="1" />
              <circle cx="100" cy="50" r="2" fill="white" stroke="#ef4444" strokeWidth="1" />
            </svg>

            <div className="absolute bottom-0 left-0 flex w-full justify-between px-4">
              {carbonWeekly.map((item) => (
                <span key={`x-${item.day}`} className="font-caption text-caption text-outline">
                  {item.day}
                </span>
              ))}
            </div>

            <div className="absolute bottom-8 left-0 w-full border-b border-surface-variant" />
            <div className="absolute bottom-[calc(8px+33%)] left-0 w-full border-b border-dashed border-surface-variant" />
            <div className="absolute bottom-[calc(8px+66%)] left-0 w-full border-b border-dashed border-surface-variant" />
          </div>
        </article>
      </section>

      <section className="rounded-[32px] border border-surface-container-highest bg-surface-container-lowest p-md shadow-[0_8px_30px_rgb(0,0,0,0.04)] lg:p-lg">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="font-h2 text-h2 text-on-surface">Historical Anomalies Log</h2>
          <div className="flex gap-2">
            <button className="rounded-lg p-2 text-outline transition-colors hover:bg-surface-container">
              <span className="material-symbols-outlined">filter_list</span>
            </button>
            <button className="rounded-lg p-2 text-outline transition-colors hover:bg-surface-container">
              <span className="material-symbols-outlined">search</span>
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-left">
            <thead>
              <tr className="border-b border-surface-variant">
                <th className="px-4 py-4 font-label-sm text-label-sm font-medium text-on-surface-variant">Date/Time</th>
                <th className="px-4 py-4 font-label-sm text-label-sm font-medium text-on-surface-variant">Room ID</th>
                <th className="px-4 py-4 font-label-sm text-label-sm font-medium text-on-surface-variant">Device</th>
                <th className="px-4 py-4 font-label-sm text-label-sm font-medium text-on-surface-variant">Wasted Power (kW)</th>
                <th className="px-4 py-4 font-label-sm text-label-sm font-medium text-on-surface-variant">Financial Loss (₺)</th>
                <th className="px-4 py-4 font-label-sm text-label-sm font-medium text-on-surface-variant">Status</th>
              </tr>
            </thead>

            <tbody className="font-body-md text-body-md text-on-surface">
              {anomalies.map((row, index) => {
                const showBottomBorder = index !== anomalies.length - 1;
                return (
                  <tr
                    key={`${row.dateTime}-${row.roomId}`}
                    className={[
                      showBottomBorder ? 'border-b border-surface-variant/50' : '',
                      'group transition-colors hover:bg-surface-container-lowest',
                    ].join(' ')}
                  >
                    <td className="px-4 py-4">{row.dateTime}</td>
                    <td className="px-4 py-4 font-medium">{row.roomId}</td>
                    <td className="px-4 py-4 text-on-surface-variant">{row.device}</td>
                    <td className="px-4 py-4">{row.wastedPowerKw}</td>
                    <td className="px-4 py-4">{row.financialLossTl}</td>
                    <td className="px-4 py-4">
                      <span className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ${getStatusClass(row.status)}`}>
                        {row.status}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        <div className="mt-4 flex justify-end">
          <button className="font-label-sm text-label-sm text-primary hover:underline">View All Logs</button>
        </div>
      </section>
    </div>
  );
}
