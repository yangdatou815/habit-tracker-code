import { Card } from "../../../components/ui/Card";
import { HabitForm, HabitList, useCreateHabitMutation } from "../../habits";
import { DashboardSummary } from "./DashboardSummary";

export function DashboardPage() {
  const createHabitMutation = useCreateHabitMutation();

  const onCreateHabit = async (payload) => {
    await createHabitMutation.mutateAsync(payload);
  };

  return (
    <main className="mx-auto max-w-3xl p-6">
      <h1 className="mb-4 text-2xl font-bold text-slate-900">Habit Tracker Dashboard</h1>
      <DashboardSummary />
      <Card className="mb-4">
        <h2 className="mb-3 text-lg font-semibold text-slate-900">Add habit</h2>
        <HabitForm onSubmit={onCreateHabit} submitLabel="Create habit" />
      </Card>
      <HabitList />
    </main>
  );
}
