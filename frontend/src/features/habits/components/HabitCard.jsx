import { useState } from "react";

import { Button } from "../../../components/ui/Button";
import { Card } from "../../../components/ui/Card";
import { useDeleteHabitMutation, useUpdateHabitMutation } from "../hooks/useHabits";
import { CompletionToggle } from "./CompletionToggle";
import { HabitForm } from "./HabitForm";
import { WeeklyHeatmap } from "./WeeklyHeatmap";

export function HabitCard({ habit }) {
  const [isEditing, setIsEditing] = useState(false);
  const updateHabitMutation = useUpdateHabitMutation();
  const deleteHabitMutation = useDeleteHabitMutation();

  const onSubmitEdit = async (payload) => {
    await updateHabitMutation.mutateAsync({ habitId: habit.id, payload });
    setIsEditing(false);
  };

  const onToggleActive = async () => {
    await updateHabitMutation.mutateAsync({
      habitId: habit.id,
      payload: { is_active: !habit.is_active },
    });
  };

  const onDelete = async () => {
    await deleteHabitMutation.mutateAsync(habit.id);
  };

  if (isEditing) {
    return (
      <Card>
        <h3 className="mb-3 text-lg font-semibold text-slate-900">Edit habit</h3>
        <HabitForm
          initialValues={habit}
          onCancel={() => setIsEditing(false)}
          onSubmit={onSubmitEdit}
          submitLabel="Update habit"
        />
      </Card>
    );
  }

  return (
    <Card className="space-y-3">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="text-lg font-semibold text-slate-900">{habit.name}</h3>
          <p className="text-sm text-slate-600">{habit.description || "No description"}</p>
          <p className="mt-1 text-xs text-slate-500">
            Target days: {habit.target_days?.length ? habit.target_days.join(", ") : "none"}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Streak: {habit.current_streak} • Longest: {habit.longest_streak} • Rate: {habit.completion_rate}%
          </p>
        </div>
        <span className="rounded-full bg-slate-100 px-2 py-1 text-xs text-slate-700">
          {habit.is_active ? "Active" : "Archived"}
        </span>
      </div>

      <WeeklyHeatmap habitId={habit.id} targetDays={habit.target_days} />

      <div className="flex flex-wrap gap-2">
        <CompletionToggle habitId={habit.id} />
        <Button className="bg-slate-500 hover:bg-slate-600" onClick={() => setIsEditing(true)} type="button">
          Edit
        </Button>
        <Button
          className="bg-slate-500 hover:bg-slate-600"
          disabled={updateHabitMutation.isPending}
          onClick={onToggleActive}
          type="button"
        >
          {habit.is_active ? "Archive" : "Unarchive"}
        </Button>
        <Button
          className="bg-slate-700 hover:bg-slate-800"
          disabled={deleteHabitMutation.isPending}
          onClick={onDelete}
          type="button"
        >
          Delete
        </Button>
      </div>
    </Card>
  );
}
