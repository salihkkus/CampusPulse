import React, { useState, useEffect, useMemo, useRef } from 'react';
import { getAvailableTimestamps } from '../services/api';

export default function DateRangeSelector({ onRangeChange }) {
  const [timestamps, setTimestamps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [startHour, setStartHour] = useState(0);
  const [endHour, setEndHour] = useState(23);

  const days = useMemo(() => {
    const uniqueDays = [...new Set(timestamps.map(ts => ts.split('T')[0]))].sort();
    return uniqueDays;
  }, [timestamps]);

  useEffect(() => {
    async function fetchDays() {
      const data = await getAvailableTimestamps();
      if (data?.timestamps) {
        setTimestamps(data.timestamps);
        const uniqueDays = [...new Set(data.timestamps.map(ts => ts.split('T')[0]))].sort();
        if (uniqueDays.length > 0) {
          setStartDate(uniqueDays[0]);
          setEndDate(uniqueDays[uniqueDays.length - 1]);
        }
      }
      setLoading(false);
    }
    fetchDays();
  }, []);

  useEffect(() => {
    if (startDate && endDate) {
      onRangeChange({ startDate, endDate, startHour, endHour });
    }
  }, [startDate, endDate, startHour, endHour, onRangeChange]);

  if (loading) return <div className="h-20 w-full animate-pulse bg-surface-container rounded-2xl" />;

  const formatDate = (dateStr) => {
    const [y, m, d] = dateStr.split('-').map(Number);
    const date = new Date(y, m - 1, d);
    return {
      dayName: date.toLocaleString('tr-TR', { weekday: 'short' }),
      dayNum: d,
      month: date.toLocaleString('tr-TR', { month: 'short' })
    };
  };

  return (
    <div className="flex flex-col gap-10 py-6">
      <div className="grid grid-cols-1 gap-10 lg:grid-cols-2">
        {/* Start Date */}
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between px-2">
            <label className="text-xs font-black uppercase tracking-[0.2em] text-primary">Başlangıç Tarihi</label>
            <span className="text-[10px] font-bold text-outline uppercase">{startDate}</span>
          </div>
          
          <div className="relative group">
            {/* Nav Arrows */}
            <div className="pointer-events-none absolute left-0 z-10 flex h-full w-12 items-center justify-start bg-gradient-to-r from-background to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
               <span className="material-symbols-outlined text-primary animate-pulse">chevron_left</span>
            </div>
            <div className="pointer-events-none absolute right-0 z-10 flex h-full w-12 items-center justify-end bg-gradient-to-l from-background to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
               <span className="material-symbols-outlined text-primary animate-pulse">chevron_right</span>
            </div>

            <div 
              className="no-scrollbar flex gap-4 overflow-x-auto pb-4 pt-2 px-2"
              style={{ cursor: 'grab' }}
              onMouseDown={(e) => {
                const el = e.currentTarget;
                el.style.cursor = 'grabbing';
                const startX = e.pageX - el.offsetLeft;
                const scrollLeft = el.scrollLeft;
                const onMouseMove = (e) => {
                  const x = e.pageX - el.offsetLeft;
                  const walk = (x - startX) * 2;
                  el.scrollLeft = scrollLeft - walk;
                };
                const onMouseUp = () => {
                  el.style.cursor = 'grab';
                  window.removeEventListener('mousemove', onMouseMove);
                  window.removeEventListener('mouseup', onMouseUp);
                };
                window.addEventListener('mousemove', onMouseMove);
                window.addEventListener('mouseup', onMouseUp);
              }}
            >
              {days.map(day => {
                const { dayName, dayNum, month } = formatDate(day);
                const isSelected = startDate === day;
                return (
                  <button
                    key={`start-${day}`}
                    onClick={() => setStartDate(day)}
                    className={`flex min-w-[75px] flex-col items-center rounded-2xl p-4 transition-all duration-300 ${isSelected ? 'bg-primary text-white shadow-xl shadow-primary/30 scale-110 z-10' : 'bg-white border border-surface-variant text-on-surface-variant hover:border-primary/50 opacity-60 hover:opacity-100'}`}
                  >
                    <span className="text-[10px] font-bold uppercase">{dayName}</span>
                    <span className="text-xl font-black my-1">{dayNum}</span>
                    <span className="text-[10px] font-bold opacity-60">{month}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* End Date */}
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between px-2">
            <label className="text-xs font-black uppercase tracking-[0.2em] text-primary">Bitiş Tarihi</label>
            <span className="text-[10px] font-bold text-outline uppercase">{endDate}</span>
          </div>

          <div className="relative group">
            {/* Nav Arrows */}
            <div className="pointer-events-none absolute left-0 z-10 flex h-full w-12 items-center justify-start bg-gradient-to-r from-background to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
               <span className="material-symbols-outlined text-primary animate-pulse">chevron_left</span>
            </div>
            <div className="pointer-events-none absolute right-0 z-10 flex h-full w-12 items-center justify-end bg-gradient-to-l from-background to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
               <span className="material-symbols-outlined text-primary animate-pulse">chevron_right</span>
            </div>

            <div 
              className="no-scrollbar flex gap-4 overflow-x-auto pb-4 pt-2 px-2"
              style={{ cursor: 'grab' }}
              onMouseDown={(e) => {
                const el = e.currentTarget;
                el.style.cursor = 'grabbing';
                const startX = e.pageX - el.offsetLeft;
                const scrollLeft = el.scrollLeft;
                const onMouseMove = (e) => {
                  const x = e.pageX - el.offsetLeft;
                  const walk = (x - startX) * 2;
                  el.scrollLeft = scrollLeft - walk;
                };
                const onMouseUp = () => {
                  el.style.cursor = 'grab';
                  window.removeEventListener('mousemove', onMouseMove);
                  window.removeEventListener('mouseup', onMouseUp);
                };
                window.addEventListener('mousemove', onMouseMove);
                window.addEventListener('mouseup', onMouseUp);
              }}
            >
              {days.map(day => {
                const { dayName, dayNum, month } = formatDate(day);
                const isSelected = endDate === day;
                return (
                  <button
                    key={`end-${day}`}
                    onClick={() => setEndDate(day)}
                    className={`flex min-w-[75px] flex-col items-center rounded-2xl p-4 transition-all duration-300 ${isSelected ? 'bg-primary text-white shadow-xl shadow-primary/30 scale-110 z-10' : 'bg-white border border-surface-variant text-on-surface-variant hover:border-primary/50 opacity-60 hover:opacity-100'}`}
                  >
                    <span className="text-[10px] font-bold uppercase">{dayName}</span>
                    <span className="text-xl font-black my-1">{dayNum}</span>
                    <span className="text-[10px] font-bold opacity-60">{month}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* Hour Range Selector */}
      <div className="flex flex-col items-center gap-6">
        <div className="flex flex-col items-center gap-2">
          <label className="text-xs font-black uppercase tracking-[0.2em] text-primary">Analiz Saat Aralığı</label>
          <div className="h-1 w-12 rounded-full bg-primary/20"></div>
        </div>

        <div className="flex flex-col items-center gap-4">
          <div className="flex items-center gap-6 rounded-[32px] bg-white p-2 shadow-[0_10px_40px_-10px_rgba(0,0,0,0.05)] border border-surface-variant/50">
            {/* Start Hour */}
            <div className="group relative flex flex-col items-center px-6 py-2 transition-all hover:bg-surface-container-low rounded-[24px]">
              <span className="text-[10px] font-bold text-outline uppercase tracking-wider mb-1">Başlangıç</span>
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined pointer-events-none text-primary text-xl transition-transform group-hover:translate-y-0.5">keyboard_arrow_down</span>
                <select 
                  value={startHour} 
                  onChange={(e) => setStartHour(Number(e.target.value))} 
                  className="appearance-none bg-transparent font-black text-xl text-on-surface focus:outline-none cursor-pointer"
                >
                  {[...Array(24)].map((_, i) => <option key={i} value={i}>{String(i).padStart(2, '0')}:00</option>)}
                </select>
              </div>
            </div>

            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/5 text-primary">
               <span className="material-symbols-outlined text-2xl">trending_flat</span>
            </div>

            {/* End Hour */}
            <div className="group relative flex flex-col items-center px-6 py-2 transition-all hover:bg-surface-container-low rounded-[24px]">
              <span className="text-[10px] font-bold text-outline uppercase tracking-wider mb-1">Bitiş</span>
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined pointer-events-none text-primary text-xl transition-transform group-hover:translate-y-0.5">keyboard_arrow_down</span>
                <select 
                  value={endHour} 
                  onChange={(e) => setEndHour(Number(e.target.value))} 
                  className="appearance-none bg-transparent font-black text-xl text-on-surface focus:outline-none cursor-pointer"
                >
                  {[...Array(24)].map((_, i) => <option key={i} value={i}>{String(i).padStart(2, '0')}:00</option>)}
                </select>
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-2 rounded-full bg-primary/5 px-4 py-1.5 border border-primary/10">
             <span className="material-symbols-outlined text-sm text-primary">history</span>
             <p className="text-[11px] font-bold text-primary/80 uppercase tracking-tighter">
               {startDate === endDate ? "Tam gün analizi için 00:00 - 23:00 seçin" : "Çoklu günlerde tüm saatler kapsanır"}
             </p>
          </div>
        </div>
      </div>

      <style>{`
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
      `}</style>
    </div>
  );
}
