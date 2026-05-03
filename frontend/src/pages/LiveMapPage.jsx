import React from 'react';
import CampusMapViewer from '../components/CampusMapViewer';
import { useApi } from '../hooks/useApi';
import { getBatchAnalysis } from '../services/api';

export default function LiveMapPage() {
  const { data: batchData, loading: batchLoading } = useApi(getBatchAnalysis, [], 30_000);
  const rooms = batchData?.data?.rooms || [];

  return (
    <div className="mx-auto flex h-full max-w-7xl flex-col gap-lg">
      <header>
        <h1 className="mb-xs font-h1 text-h1 text-on-background">Canlı 3D Harita</h1>
        <p className="font-body-lg text-body-lg text-on-surface-variant">
          Etkileşimli kampüs enerji tüketimi ve israf analizi.
        </p>
      </header>

      <CampusMapViewer
        rooms={rooms}
        loading={batchLoading}
        minHeight="600px"
        maxPanelH="800px"
      />
    </div>
  );
}
