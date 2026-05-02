export const apiResponseData = {
  instant_loss_tl_per_hour: 3.0,
  daily_cost_tl: 72.0,
  carbon_kg_per_hour: 0.54,
  diagnostic_message: '101 nolu odada muhtemelen klima açık unutulmuş.',
  primary_device: 'klima',
  device_cost_breakdown: {
    klima: {
      hourly_cost_tl: 3.0,
      carbon_kg_per_hour: 0.54,
    },
    aydinlatma: {
      hourly_cost_tl: 1.2,
      carbon_kg_per_hour: 0.15,
    },
    projeksiyon: {
      hourly_cost_tl: 0.8,
      carbon_kg_per_hour: 0.08,
    },
  },
};

const deviceLabels = {
  klima: 'Klima',
  aydinlatma: 'Aydınlatma',
  projeksiyon: 'Projeksiyon',
};

const deviceSections = {
  klima: 'Soğutma & İklimlendirme',
  aydinlatma: 'Aydınlatma',
  projeksiyon: 'AV Ekipmanları',
};

const deviceColors = {
  klima: '#FFADAD',
  aydinlatma: '#CAFFBF',
  projeksiyon: '#9BF6FF',
};

export const getDeviceCostBreakdownChart = () =>
  Object.entries(apiResponseData.device_cost_breakdown).map(([key, value]) => ({
    key,
    name: deviceLabels[key] ?? key,
    value: value.hourly_cost_tl,
    carbon: value.carbon_kg_per_hour,
    section: deviceSections[key] ?? 'Diğer Ekipmanlar',
    color: deviceColors[key] ?? '#6B7280',
  }));

export const dashboardAlerts = [
  {
    title: '101 nolu odada muhtemelen klima açık unutulmuş.',
    label: 'klima',
    location: 'Oda 101',
    severity: 'Kritik',
    time: 'Şimdi',
    icon: 'warning',
    tone: 'error',
  },
  {
    title: 'Açık Işıklar (Boş Oda)',
    label: 'aydınlatma',
    location: 'Amfi A',
    severity: '-₺45',
    time: '4s önce',
    icon: 'lightbulb',
    tone: 'amber',
  },
  {
    title: 'Boşta Çalışan Ekipman',
    label: 'projeksiyon',
    location: 'Kütüphane Kat 2',
    severity: '-₺20',
    time: '5s önce',
    icon: 'desktop_windows',
    tone: 'blue',
  },
];

export const navigationItems = [
  { label: 'Gösterge Paneli', icon: 'dashboard', path: '/', end: true },
  { label: 'Oda Durumları', icon: 'meeting_room', path: '/rooms' },
  { label: '3D Canlı Harita', icon: 'map', path: '/live-map' },
  { label: 'Raporlar', icon: 'assessment', path: '/reports' },

];
