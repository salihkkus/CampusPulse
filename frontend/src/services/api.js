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
export async function getFrontendRooms() {
  return fetchJSON(`${BASE_URL}/v1/frontend/rooms`);
}

// ─── Frontend Alerts ─────────────────────────────────────────
export async function getFrontendAlerts() {
  return fetchJSON(`${BASE_URL}/v1/frontend/alerts`);
}

// ─── Charts ──────────────────────────────────────────────────
export async function getDashboardCharts() {
  return fetchJSON(`${BASE_URL}/v1/charts/dashboard`);
}

// ─── Room History ────────────────────────────────────────────
export async function getRoomHistory(roomId, hours = 24) {
  return fetchJSON(`${BASE_URL}/v1/rooms/${roomId}/history?hours=${hours}`);
}

// ─── Financial Summary ──────────────────────────────────────
export async function getFinancialSummary() {
  return fetchJSON(`${BASE_URL}/v1/financial/summary`);
}

// ─── Energy Audit Report ────────────────────────────────────
export async function getEnergyAuditReport() {
  return fetchJSON(`${BASE_URL}/v1/reports/energy-audit`);
}
