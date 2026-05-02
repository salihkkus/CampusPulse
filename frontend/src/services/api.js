const BASE_URL = '/api';

async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${res.statusText}`);
  }
  return res.json();
}

// ─── Dashboard Summary ───────────────────────────────────────
export async function getDashboardSummary() {
  return fetchJSON(`${BASE_URL}/v2/ai/dashboard-summary`);
}

// ─── All Rooms Batch Analysis ────────────────────────────────
export async function getBatchAnalysis() {
  return fetchJSON(`${BASE_URL}/v2/ai/batch-analysis`);
}

// ─── Single Room Status with AI ──────────────────────────────
export async function getRoomStatus(roomId) {
  return fetchJSON(`${BASE_URL}/v2/ai/room-status/${roomId}`);
}

// ─── Quick Diagnosis ─────────────────────────────────────────
export async function getQuickDiagnosis(roomId) {
  return fetchJSON(`${BASE_URL}/v2/ai/quick-diagnosis/${roomId}`);
}

// ─── Model Info ──────────────────────────────────────────────
export async function getModelInfo() {
  return fetchJSON(`${BASE_URL}/v2/ai/model-info`);
}

// ─── Frontend Optimized Rooms ────────────────────────────────
export async function getFrontendRooms(timestamp = null) {
  const url = timestamp ? `${BASE_URL}/v1/frontend/rooms?timestamp=${timestamp}` : `${BASE_URL}/v1/frontend/rooms`;
  return fetchJSON(url);
}

// ─── Frontend Alerts ─────────────────────────────────────────
export async function getFrontendAlerts(timestamp = null) {
  const url = timestamp ? `${BASE_URL}/v1/frontend/alerts?timestamp=${timestamp}` : `${BASE_URL}/v1/frontend/alerts`;
  return fetchJSON(url);
}

// ─── Frontend Summary ─────────────────────────────────────────
export async function getFrontendSummary(timestamp = null) {
  const url = timestamp ? `${BASE_URL}/v1/frontend/summary?timestamp=${timestamp}` : `${BASE_URL}/v1/frontend/summary`;
  return fetchJSON(url);
}

// ─── Available Timestamps ────────────────────────────────────
export async function getAvailableTimestamps() {
  return fetchJSON(`${BASE_URL}/v1/frontend/timestamps`);
}

// ─── Range Report ───────────────────────────────────────────
export async function getRangeReport(startDate, endDate, startHour = 0, endHour = 23) {
  return fetchJSON(`${BASE_URL}/v1/frontend/range-report?start_date=${startDate}&end_date=${endDate}&start_hour=${startHour}&end_hour=${endHour}`);
}

// ─── Charts ──────────────────────────────────────────────────
export async function getDashboardCharts() {
  return fetchJSON(`${BASE_URL}/v1/charts/dashboard`);
}

// ─── Room History ────────────────────────────────────────────
export async function getRoomHistory(roomId, hours = 24, timestamp = null) {
  let url = `${BASE_URL}/v1/rooms/${roomId}/history?hours=${hours}`;
  if (timestamp) url += `&timestamp=${timestamp}`;
  return fetchJSON(url);
}

// ─── Financial Summary ──────────────────────────────────────
export async function getFinancialSummary() {
  return fetchJSON(`${BASE_URL}/v1/financial/summary`);
}

// ─── Energy Audit Report ────────────────────────────────────
export async function getEnergyAuditReport() {
  return fetchJSON(`${BASE_URL}/v1/reports/energy-audit`);
}
