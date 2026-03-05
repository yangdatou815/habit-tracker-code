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

export function fetchStatsOverview({ from, to } = {}) {
  return request(withSearchParams("/v1/stats/overview", { from, to }));
}
