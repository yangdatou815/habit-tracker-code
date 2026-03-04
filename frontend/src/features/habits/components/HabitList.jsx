import { useState } from "react";

import { Card } from "../../../components/ui/Card";
import { useHabitsQuery } from "../hooks/useHabits";
import { HabitCard } from "./HabitCard";

export function HabitList() {
  const [showArchived, setShowArchived] = useState(false);
  const habitsQuery = useHabitsQuery({
    isActive: showArchived ? undefined : true,
  });

  return (
    <Card className="space-y-3">
      <div className="flex items-center justify-between gap-2">
        <h2 className="text-lg font-semibold text-slate-900">Habits</h2>
        <label className="flex items-center gap-2 text-sm text-slate-700">
          <input
            checked={showArchived}
            onChange={(event) => setShowArchived(event.target.checked)}
            type="checkbox"
          />
          Show archived
        </label>
      </div>

      {habitsQuery.isLoading ? <p className="text-sm text-slate-600">Loading habits...</p> : null}
      {habitsQuery.isError ? <p className="text-sm text-red-600">Unable to load habits.</p> : null}

      {!habitsQuery.isLoading && !habitsQuery.isError && habitsQuery.data?.length === 0 ? (
        <p className="text-sm text-slate-600">No habits yet. Add your first one above.</p>
      ) : null}

      <div className="space-y-3">
        {(habitsQuery.data || []).map((habit) => (
          <HabitCard habit={habit} key={habit.id} />
        ))}
      </div>
    </Card>
  );
}
