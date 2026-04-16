import { request } from "../../lib/api";

// ── Projects ─────────────────────────────────────────────────

export function listProjects(isActive) {
  const params = new URLSearchParams();
  if (isActive !== undefined && isActive !== null) {
    params.set("is_active", String(isActive));
  }
  const qs = params.toString();
  return request(`/v1/projects${qs ? `?${qs}` : ""}`);
}

export function createProject(data) {
  return request("/v1/projects", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function updateProject(id, data) {
  return request(`/v1/projects/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export function deleteProject(id) {
  return request(`/v1/projects/${id}`, {
    method: "DELETE",
  });
}

// ── Checkins ─────────────────────────────────────────────────

export function toggleCheckin(projectId, date, status) {
  return request(`/v1/checkins/${projectId}/${date}`, {
    method: "PUT",
    body: JSON.stringify({ status }),
  });
}

export function getTodayCheckins() {
  return request("/v1/checkins/today");
}

export function getDateCheckins(date) {
  return request(`/v1/checkins/date/${date}`);
}

export function getHistory(fromDate, toDate) {
  return request(`/v1/checkins/history?from_date=${fromDate}&to_date=${toDate}`);
}
