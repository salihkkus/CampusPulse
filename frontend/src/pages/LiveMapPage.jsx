import React, { useState } from 'react';
import ThreeDMap from '../components/ThreeDMap';
import RoomStatusCard from '../components/RoomStatusCard';
import { useApi } from '../hooks/useApi';
import { getBatchAnalysis } from '../services/api';

export default function LiveMapPage() {
  const [activeBuilding, setActiveBuilding] = useState(null);
  
  const { data: batchData, loading: batchLoading } = useApi(getBatchAnalysis, [], 30_000);
  const rooms = batchData?.data?.rooms || [];

  const handleBuildingClick = (buildingName) => {
    setActiveBuilding(buildingName === activeBuilding ? null : buildingName);
  };

  const displayedRooms = rooms.filter(room => {
    if (activeBuilding === "Mühendislik 1") return room.room_id.startsWith("M1_");
    if (activeBuilding === "Mühendislik 2") return room.room_id.startsWith("M2_");
    if (activeBuilding === "AKM") return room.room_id.startsWith("AKM_");
    return false;
  }).sort((a, b) => {
    if (a.status === 'CRITICAL' && b.status !== 'CRITICAL') return -1;
    if (b.status === 'CRITICAL' && a.status !== 'CRITICAL') return 1;
    return 0;
  });

  const criticalBuildings = [];
  if (rooms.some(r => r.status === 'CRITICAL' && r.room_id.startsWith("M1_"))) criticalBuildings.push("Mühendislik 1");
  if (rooms.some(r => r.status === 'CRITICAL' && r.room_id.startsWith("M2_"))) criticalBuildings.push("Mühendislik 2");
  if (rooms.some(r => r.status === 'CRITICAL' && r.room_id.startsWith("AKM_"))) criticalBuildings.push("AKM");

  return (
    <div className="mx-auto flex h-full max-w-7xl flex-col gap-lg">
      <header>
        <h1 className="mb-xs font-h1 text-h1 text-on-background">Canlı 3D Harita</h1>
        <p className="font-body-lg text-body-lg text-on-surface-variant">
          Etkileşimli kampüs termal ve enerji analizi.
        </p>
      </header>

      <div className="flex flex-col gap-6 lg:flex-row h-full">
        {/* The 3D Viewer Card */}
        <div className={`flex flex-col rounded-3xl border border-outline-variant/30 bg-surface-container-lowest p-6 shadow-md transition-all duration-500 ease-in-out ${activeBuilding ? 'lg:w-2/3' : 'w-full'}`}>
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h2 className="font-h2 text-h2 text-on-background">Canlı 3D Dijital İkiz</h2>
              <p className="font-body-md text-body-md text-on-surface-variant">
                Gerçek zamanlı termal ve enerji haritalaması. Binalara tıklayarak detayları görebilirsiniz.
              </p>
            </div>
            <div className="flex items-center gap-2 rounded-full border border-error-container bg-error-container/50 px-3 py-1.5 font-label-sm text-on-error-container backdrop-blur-sm">
              <span className="h-2 w-2 animate-pulse rounded-full bg-error"></span>
              • Yüksek Tüketim
            </div>
          </div>

          <div className="relative flex min-h-[600px] flex-1 flex-col items-center justify-center overflow-hidden rounded-2xl border border-outline-variant/50 bg-surface-container">
            <ThreeDMap 
              onBuildingClick={handleBuildingClick} 
              activeBuilding={activeBuilding} 
              criticalBuildings={criticalBuildings}
            />
          </div>
        </div>

        {/* Side Panel for Selected Building */}
        {activeBuilding && (
          <div className="flex flex-col gap-4 lg:w-1/3 max-h-[800px]">
            <div className="rounded-3xl border border-outline-variant/30 bg-surface-container-lowest p-6 shadow-md h-full flex flex-col">
              <div className="flex items-center justify-between mb-4 border-b border-outline-variant/50 pb-4">
                <h2 className="font-h2 text-h2 text-on-background">{activeBuilding} Odaları</h2>
                <button 
                  onClick={() => setActiveBuilding(null)}
                  className="flex h-8 w-8 items-center justify-center rounded-full hover:bg-surface-variant transition-colors"
                >
                  <span className="material-symbols-outlined text-[20px]">close</span>
                </button>
              </div>
              
              <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
                {batchLoading ? (
                  <div className="flex justify-center p-8">
                    <span className="material-symbols-outlined animate-spin text-primary text-4xl">autorenew</span>
                  </div>
                ) : displayedRooms.length > 0 ? (
                  <div className="flex flex-col gap-4 pb-4">
                    {displayedRooms.map(room => (
                      <RoomStatusCard key={room.room_id} room={room} />
                    ))}
                  </div>
                ) : (
                  <div className="flex flex-col items-center justify-center p-8 text-center text-on-surface-variant h-full">
                    <span className="material-symbols-outlined text-[48px] mb-4 opacity-50">meeting_room</span>
                    <p className="font-medium">Bu binaya ait canlı veri bulunamadı.</p>
                    <p className="text-sm opacity-75 mt-2">Şu anki izleme sensörleri tüm kampüs binalarında aktiftir.</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
