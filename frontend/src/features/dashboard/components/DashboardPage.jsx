import { HabitListPlaceholder } from "../../habits/components/HabitListPlaceholder";
import { Card } from "../../../components/ui/Card";

export function DashboardPage() {
  return (
    <main className="mx-auto max-w-3xl p-6">
      <h1 className="mb-4 text-2xl font-bold text-slate-900">Habit Tracker Dashboard</h1>
      <Card className="mb-4">
        <p className="text-sm text-slate-700">Foundation scaffold complete. Metrics and actions arrive in Phase 2.</p>
      </Card>
      <HabitListPlaceholder />
    </main>
  );
}
