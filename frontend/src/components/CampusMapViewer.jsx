import React, { useState, useMemo, useCallback } from 'react';
import ThreeDMap from './ThreeDMap';
import RoomStatusCard from './RoomStatusCard';

/**
 * CampusMapViewer — Birleştirilmiş 3D Kampüs Harita bileşeni.
 * 
 * Hem Dashboard hem de Canlı Harita sayfasında kullanılır.
 * 3D simülasyonu, bina tıklama etkileşimini ve oda panelini
 * tek bir bileşende yönetir.
 * 
 * Props:
 *   rooms      — Oda nesneleri dizisi ({ room_id, status, building?, ... })
 *   loading    — Veriler yüklenirken true
 *   minHeight  — 3D görüntüleyicinin minimum yüksekliği (varsayılan: '500px')
 *   maxPanelH  — Yan panelin max yüksekliği (varsayılan: '700px')
 *   className  — Kapsayıcı ek class (opsiyonel)
 */
export default function CampusMapViewer({
  rooms = [],
  loading = false,
  minHeight = '500px',
  maxPanelH = '700px',
  className = '',
}) {
  const [activeBuilding, setActiveBuilding] = useState(null);

  // ── Bina tıklama ──────────────────────────────────────
  const handleBuildingClick = useCallback((buildingName) => {
    setActiveBuilding(prev => prev === buildingName ? null : buildingName);
  }, []);

  // ── Kritik bina listesi (memoized) ────────────────────
  const criticalBuildings = useMemo(() => {
    const result = [];
    if (rooms.some(r => (r.status === 'CRITICAL' || r.status === 'WARNING') && r.room_id.startsWith('M1_'))) {
      result.push('Mühendislik 1');
    }
    if (rooms.some(r => (r.status === 'CRITICAL' || r.status === 'WARNING') && r.room_id.startsWith('M2_'))) {
      result.push('Mühendislik 2');
    }
    if (rooms.some(r => (r.status === 'CRITICAL' || r.status === 'WARNING') && r.room_id.startsWith('AKM_'))) {
      result.push('AKM');
    }
    return result;
  }, [rooms]);

  // ── Seçilen binaya ait odalar (memoized) ──────────────
  const displayedRooms = useMemo(() => {
    return rooms
      .filter((room) => {
        if (activeBuilding === 'Mühendislik 1') return room.room_id.startsWith('M1_');
        if (activeBuilding === 'Mühendislik 2') return room.room_id.startsWith('M2_');
        if (activeBuilding === 'AKM') return room.room_id.startsWith('AKM_');
        return false;
      })
      .sort((a, b) => {
        if (a.status === 'CRITICAL' && b.status !== 'CRITICAL') return -1;
        if (b.status === 'CRITICAL' && a.status !== 'CRITICAL') return 1;
        if (a.status === 'WARNING' && b.status !== 'WARNING') return -1;
        if (b.status === 'WARNING' && a.status !== 'WARNING') return 1;
        return 0;
      });
  }, [rooms, activeBuilding]);

  return (
    <section className={`flex flex-col gap-6 lg:flex-row h-full ${className}`}>
      {/* ── 3D Görüntüleyici Kartı ──────────────────── */}
      <div
        className={`flex flex-col rounded-3xl border border-outline-variant/30 bg-surface-container-lowest p-6 shadow-md transition-all duration-500 ease-in-out ${
          activeBuilding ? 'lg:w-2/3' : 'w-full'
        }`}
      >
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h2 className="font-h2 text-h2 text-on-background">Canlı 3D Dijital İkiz</h2>
            <p className="mt-1 font-body-md text-body-md text-on-surface-variant">
              Kampüs enerji tüketimi ve israf takibi. Binalara tıklayarak detayları görebilirsiniz.
            </p>
          </div>
          <div className="flex items-center gap-2 rounded-full border border-error-container bg-error-container/50 px-3 py-1.5 font-label-sm text-on-error-container backdrop-blur-sm">
            <span className="h-2 w-2 animate-pulse rounded-full bg-error"></span>
            • Yüksek Tüketim
          </div>
        </div>

        <div
          className="relative flex flex-1 flex-col items-center justify-center overflow-hidden rounded-2xl border border-outline-variant/50 bg-surface-container"
          style={{ minHeight }}
        >
          <ThreeDMap
            onBuildingClick={handleBuildingClick}
            activeBuilding={activeBuilding}
            criticalBuildings={criticalBuildings}
          />
        </div>
      </div>

      {/* ── Bina Oda Paneli ─────────────────────────── */}
      {activeBuilding && (
        <div className="flex flex-col gap-4 lg:w-1/3" style={{ maxHeight: maxPanelH }}>
          <div className="rounded-3xl border border-outline-variant/30 bg-surface-container-lowest p-6 shadow-md h-full flex flex-col">
            <div className="flex items-center justify-between mb-4 border-b border-outline-variant/50 pb-4">
              <h2 className="font-h2 text-h2 text-on-background">{activeBuilding} Odaları</h2>
              <button
                onClick={() => setActiveBuilding(null)}
                className="flex h-8 w-8 items-center justify-center rounded-full hover:bg-surface-variant transition-colors text-on-surface"
              >
                <span className="material-symbols-outlined text-[20px]">close</span>
              </button>
            </div>

            <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
              {loading ? (
                <div className="flex justify-center p-8">
                  <span className="material-symbols-outlined animate-spin text-primary text-4xl">autorenew</span>
                </div>
              ) : displayedRooms.length > 0 ? (
                <div className="flex flex-col gap-4 pb-4">
                  {displayedRooms.map((room) => (
                    <RoomStatusCard key={room.room_id} room={room} />
                  ))}
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center p-8 text-center text-on-surface-variant h-full">
                  <span className="material-symbols-outlined text-[48px] mb-4 opacity-50">meeting_room</span>
                  <p className="font-medium">Bu binaya ait canlı veri bulunamadı.</p>
                  <p className="text-sm opacity-75 mt-2">
                    Şu anki izleme sensörleri tüm kampüs binalarında aktiftir.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
