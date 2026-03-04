import { request } from "../../../lib/api";

function withSearchParams(path, params) {
  const searchParams = new URLSearchParams();

  Object.entries(params || {}).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      searchParams.set(key, String(value));
    }
  });

  const queryString = searchParams.toString();
  return queryString ? `${path}?${queryString}` : path;
}

export function fetchHabits({ isActive } = {}) {
  return request(withSearchParams("/v1/habits", { is_active: isActive }));
}

export function fetchHabit(habitId) {
  return request(`/v1/habits/${habitId}`);
}

export function createHabit(payload) {
  return request("/v1/habits", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateHabit(habitId, payload) {
  return request(`/v1/habits/${habitId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function deleteHabit(habitId) {
  return request(`/v1/habits/${habitId}`, {
    method: "DELETE",
  });
}

export function fetchHabitCompletions(habitId, { from, to } = {}) {
  return request(withSearchParams(`/v1/habits/${habitId}/completions`, { from, to }));
}

export function upsertHabitCompletion(habitId, completedDate, status) {
  return request(`/v1/habits/${habitId}/completions/${completedDate}`, {
    method: "PUT",
    body: JSON.stringify({ status }),
  });
}
