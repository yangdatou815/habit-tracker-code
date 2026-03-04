import { Card } from "../../../components/ui/Card";

export function HabitListPlaceholder() {
  return (
    <Card>
      <h2 className="text-lg font-semibold text-slate-900">Habits</h2>
      <p className="mt-2 text-sm text-slate-600">No habits yet. Habit list will appear here in Phase 2.</p>
    </Card>
  );
}
