import { Card } from "../../../components/ui/Card";
import { useStatsOverviewQuery } from "../hooks/useStats";

export function DashboardSummary() {
  const statsQuery = useStatsOverviewQuery();
  const stats = statsQuery.data;

  if (statsQuery.isLoading) {
    return (
      <Card className="mb-4">
        <p className="text-sm text-slate-600">Loading stats...</p>
      </Card>
    );
  }

  if (statsQuery.isError || !stats) {
    return null;
  }

  return (
    <Card className="mb-4 flex items-center justify-between gap-4">
      <div>
        <p className="text-sm font-medium text-slate-600">Today</p>
        <p className="text-2xl font-bold text-slate-900">
          {stats.completed_today}
          <span className="text-base font-normal text-slate-500">/{stats.total_today}</span>
        </p>
      </div>
      <div>
        <p className="text-sm font-medium text-slate-600">7-day rate</p>
        <p className="text-2xl font-bold text-emerald-600">{stats.completion_rate}%</p>
      </div>
      <div>
        <p className="text-sm font-medium text-slate-600">Active habits</p>
        <p className="text-2xl font-bold text-slate-900">{stats.total_habits}</p>
      </div>
    </Card>
  );
}
