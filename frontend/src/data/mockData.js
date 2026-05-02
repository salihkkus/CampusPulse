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
  klima: 'Cooling & HVAC',
  aydinlatma: 'Lighting',
  projeksiyon: 'AV Equipment',
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
    section: deviceSections[key] ?? 'Other Equipment',
    color: deviceColors[key] ?? '#6B7280',
  }));

export const dashboardAlerts = [
  {
    title: '101 nolu odada muhtemelen klima açık unutulmuş.',
    label: 'klima',
    location: 'Room 101',
    severity: 'Critical',
    time: 'Now',
    icon: 'warning',
    tone: 'error',
  },
  {
    title: 'Lights On (Empty Room)',
    label: 'aydınlatma',
    location: 'Lecture Hall A',
    severity: '-₺45',
    time: '4h ago',
    icon: 'lightbulb',
    tone: 'amber',
  },
  {
    title: 'Idle Workstations',
    label: 'projeksiyon',
    location: 'Library Fl 2',
    severity: '-₺20',
    time: '5h ago',
    icon: 'desktop_windows',
    tone: 'blue',
  },
];

export const navigationItems = [
  { label: 'Dashboard', icon: 'dashboard', path: '/', end: true },
  { label: '3D Live Map', icon: 'map', path: '/live-map' },
  { label: 'Reports', icon: 'assessment', path: '/reports' },
  { label: 'Schedules', icon: 'calendar_today', path: '/schedules' },
];
