import React, { useState, useEffect, useMemo, useRef } from 'react';
import { getAvailableTimestamps } from '../services/api';

export default function TimeSelector({ onTimeChange, selectedTime }) {
  const [timestamps, setTimestamps] = useState([]);
  const [loading, setLoading] = useState(true);
  const scrollRef = useRef(null);

  // Group and sort timestamps by local day
  const groupedTimes = useMemo(() => {
    const groups = {};
    
    // Sort all timestamps chronologically first
    const sortedTs = [...timestamps].sort((a, b) => new Date(a) - new Date(b));
    
    sortedTs.forEach(ts => {
      const localDate = new Date(ts);
      // Create a local date string (YYYY-MM-DD)
      const dateKey = localDate.getFullYear() + '-' + 
                      String(localDate.getMonth() + 1).padStart(2, '0') + '-' + 
                      String(localDate.getDate()).padStart(2, '0');
                      
      if (!groups[dateKey]) groups[dateKey] = [];
      groups[dateKey].push(ts);
    });
    
    // Within each day, sort by actual time
    Object.keys(groups).forEach(day => {
      groups[day].sort((a, b) => new Date(a) - new Date(b));
    });
    
    return groups;
  }, [timestamps]);

  const days = useMemo(() => Object.keys(groupedTimes).sort(), [groupedTimes]);
  
  // Determine currently selected day based on local time
  const selectedDay = useMemo(() => {
    if (!selectedTime) return days.length > 0 ? days[days.length - 1] : null;
    const d = new Date(selectedTime);
    return d.getFullYear() + '-' + 
           String(d.getMonth() + 1).padStart(2, '0') + '-' + 
           String(d.getDate()).padStart(2, '0');
  }, [selectedTime, days]);

  useEffect(() => {
    async function fetchTimestamps() {
      try {
        const data = await getAvailableTimestamps();
        if (data && data.timestamps) {
          setTimestamps(data.timestamps);
          if (!selectedTime && data.timestamps.length > 0) {
            onTimeChange(data.timestamps[data.timestamps.length - 1]);
          }
        }
      } catch (err) {
        console.error('Error fetching timestamps:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchTimestamps();
  }, [onTimeChange, selectedTime]);

  // Center the selected day in the carousel without shifting the whole page
  useEffect(() => {
    if (selectedDay && scrollRef.current) {
      const container = scrollRef.current;
      const el = document.getElementById(`day-${selectedDay}`);
      if (el) {
        const containerWidth = container.offsetWidth;
        const elOffsetLeft = el.offsetLeft;
        const elWidth = el.offsetWidth;
        
        // Calculate the position to center the element
        const scrollPosition = elOffsetLeft - (containerWidth / 2) + (elWidth / 2);
        
        container.scrollTo({
          left: scrollPosition,
          behavior: 'smooth'
        });
      }
    }
  }, [selectedDay]);

  if (loading) return (
    <div className="mx-auto flex flex-col items-center gap-4 py-8 animate-pulse">
      <div className="h-16 w-64 rounded-2xl bg-surface-container"></div>
      <div className="h-10 w-full max-w-md rounded-xl bg-surface-container-low"></div>
    </div>
  );

  const formatDate = (dateStr) => {
    // dateStr is YYYY-MM-DD
    const [y, m, d] = dateStr.split('-').map(Number);
    const date = new Date(y, m - 1, d);
    return {
      dayName: date.toLocaleString('tr-TR', { weekday: 'short' }),
      dayNum: date.getDate(),
      month: date.toLocaleString('tr-TR', { month: 'short' })
    };
  };

  const formatHour = (ts) => {
    const date = new Date(ts);
    return date.getHours().toString().padStart(2, '0') + ':00';
  };

  return (
    <div className="mx-auto flex w-full max-w-4xl flex-col items-center gap-8 py-8">
      {/* ── Day Wheel/Carousel ────────────────────────── */}
      <div className="group relative w-full overflow-hidden px-10">
        {/* Navigation Indicators */}
        <div className="pointer-events-none absolute left-0 z-10 flex h-full w-24 items-center justify-start bg-gradient-to-r from-white to-transparent opacity-100 dark:from-slate-900">
           <span className="material-symbols-outlined ml-4 animate-bounce-x text-primary opacity-30">chevron_left</span>
        </div>
        <div className="pointer-events-none absolute right-0 z-10 flex h-full w-24 items-center justify-end bg-gradient-to-l from-white to-transparent opacity-100 dark:from-slate-900">
           <span className="material-symbols-outlined mr-4 animate-bounce-x-reverse text-primary opacity-30">chevron_right</span>
        </div>
        
        <div 
          ref={scrollRef}
          className="no-scrollbar flex items-center gap-6 overflow-x-auto px-[35%] pb-6 pt-4"
          style={{ scrollSnapType: 'x mandatory', cursor: 'grab' }}
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
          {days.map((day) => {
            const { dayName, dayNum, month } = formatDate(day);
            const isSelected = selectedDay === day;
            return (
              <button
                key={day}
                id={`day-${day}`}
                onClick={() => {
                  if (selectedDay !== day) {
                    const dayTimes = groupedTimes[day];
                    // Keep the same hour if possible, else pick last
                    const currentHour = selectedTime ? new Date(selectedTime).getHours() : -1;
                    let targetTs = dayTimes.find(ts => new Date(ts).getHours() === currentHour);
                    if (!targetTs) targetTs = dayTimes[dayTimes.length - 1];
                    onTimeChange(targetTs);
                  }
                }}
                className={`flex min-w-[80px] flex-col items-center justify-center rounded-[24px] p-4 transition-all duration-500
                  ${isSelected 
                    ? 'scale-125 bg-primary text-on-primary shadow-[0_15px_30px_-5px_rgba(70,72,212,0.4)] z-20' 
                    : 'bg-surface-container text-on-surface-variant hover:bg-surface-variant hover:opacity-100 opacity-40 scale-90'
                  }`}
                style={{ scrollSnapAlign: 'center' }}
              >
                <span className={`text-[10px] font-bold uppercase tracking-widest ${isSelected ? 'opacity-100' : 'opacity-70'}`}>{dayName}</span>
                <span className="text-2xl font-black leading-none my-1">{dayNum}</span>
                <span className="text-[10px] font-bold opacity-60">{month}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* ── Hour Grid ────────────────────────────────── */}
      <div className="relative flex w-full flex-col items-center gap-4">
        <div className="h-px w-full max-w-md bg-gradient-to-r from-transparent via-outline-variant to-transparent opacity-50"></div>
        <div className="flex w-full flex-wrap justify-center gap-3 px-6">
          {selectedDay && groupedTimes[selectedDay]?.map((ts) => {
            const isSelected = selectedTime === ts;
            return (
              <button
                key={ts}
                onClick={() => onTimeChange(ts)}
                className={`group relative flex h-12 w-20 items-center justify-center rounded-2xl text-sm font-bold transition-all duration-300 border-2
                  ${isSelected 
                    ? 'bg-primary border-primary text-white shadow-lg shadow-primary/20 scale-110' 
                    : 'bg-white border-surface-container text-on-surface-variant hover:border-primary/30 hover:bg-primary/5'
                  }`}
              >
                {formatHour(ts)}
                {isSelected && (
                   <div className="absolute -bottom-1 h-1.5 w-1.5 rounded-full bg-white shadow-sm"></div>
                )}
              </button>
            );
          })}
        </div>
      </div>

      <style>{`
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
        @keyframes bounce-x {
          0%, 100% { transform: translateX(0); }
          50% { transform: translateX(-5px); }
        }
        @keyframes bounce-x-reverse {
          0%, 100% { transform: translateX(0); }
          50% { transform: translateX(5px); }
        }
        .animate-bounce-x { animation: bounce-x 1.5s infinite; }
        .animate-bounce-x-reverse { animation: bounce-x-reverse 1.5s infinite; }
      `}</style>
    </div>
  );
}
