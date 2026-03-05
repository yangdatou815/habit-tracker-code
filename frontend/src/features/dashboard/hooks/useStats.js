import { useQuery } from "@tanstack/react-query";

import { fetchStatsOverview } from "../api/stats";

export const statsQueryKeys = {
  all: ["stats"],
  overview: (from, to) => ["stats", "overview", from ?? "default", to ?? "default"],
};

export function useStatsOverviewQuery({ from, to } = {}) {
  return useQuery({
    queryKey: statsQueryKeys.overview(from, to),
    queryFn: () => fetchStatsOverview({ from, to }),
  });
}
