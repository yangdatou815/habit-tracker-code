import { Button } from "../../../components/ui/Button";
import { useCompletionsQuery, useUpsertCompletionMutation } from "../hooks/useHabits";

export function formatLocalDate(dateValue = new Date()) {
  const year = dateValue.getFullYear();
  const month = String(dateValue.getMonth() + 1).padStart(2, "0");
  const day = String(dateValue.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

export function CompletionToggle({ habitId }) {
  const completedDate = formatLocalDate();
  const completionsQuery = useCompletionsQuery(habitId, {
    from: completedDate,
    to: completedDate,
  });
  const completionMutation = useUpsertCompletionMutation();

  const existingCompletion = completionsQuery.data?.completions?.[0];
  const currentStatus = existingCompletion?.status || "not_done";
  const isDone = currentStatus === "done";

  const onToggle = async () => {
    await completionMutation.mutateAsync({
      habitId,
      completedDate,
      status: isDone ? "not_done" : "done",
    });
  };

  return (
    <Button
      className={isDone ? "bg-emerald-700 hover:bg-emerald-800" : "bg-slate-500 hover:bg-slate-600"}
      disabled={completionMutation.isPending || completionsQuery.isLoading}
      onClick={onToggle}
      type="button"
    >
      {completionMutation.isPending
        ? "Updating..."
        : isDone
          ? "Marked done"
          : "Mark done"}
    </Button>
  );
}
