import { useMemo, useState } from "react";

import { Button } from "../../../components/ui/Button";

const DAY_OPTIONS = [
  { value: "mon", label: "Mon" },
  { value: "tue", label: "Tue" },
  { value: "wed", label: "Wed" },
  { value: "thu", label: "Thu" },
  { value: "fri", label: "Fri" },
  { value: "sat", label: "Sat" },
  { value: "sun", label: "Sun" },
];

function getInitialState(initialValues) {
  return {
    name: initialValues?.name || "",
    description: initialValues?.description || "",
    target_days: initialValues?.target_days || [],
    is_active: initialValues?.is_active ?? true,
  };
}

export function HabitForm({
  initialValues,
  onSubmit,
  submitLabel = "Save Habit",
  onCancel,
}) {
  const [formState, setFormState] = useState(() => getInitialState(initialValues));
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const isEditing = useMemo(() => Boolean(initialValues), [initialValues]);

  const onChangeField = (field, value) => {
    setFormState((previous) => ({ ...previous, [field]: value }));
  };

  const toggleDay = (day) => {
    setFormState((previous) => {
      if (previous.target_days.includes(day)) {
        return { ...previous, target_days: previous.target_days.filter((item) => item !== day) };
      }

      return { ...previous, target_days: [...previous.target_days, day] };
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const trimmedName = formState.name.trim();
    if (!trimmedName) {
      setError("Habit name is required.");
      return;
    }

    setError("");
    setIsSubmitting(true);
    try {
      await onSubmit({
        name: trimmedName,
        description: formState.description.trim() || null,
        target_days: formState.target_days,
        is_active: formState.is_active,
      });

      if (!isEditing) {
        setFormState(getInitialState());
      }
    } catch {
      setError("Unable to save habit. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form className="space-y-3" onSubmit={handleSubmit}>
      <div>
        <label className="mb-1 block text-sm font-medium text-slate-700" htmlFor="habit-name">
          Habit name
        </label>
        <input
          id="habit-name"
          className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
          value={formState.name}
          onChange={(event) => onChangeField("name", event.target.value)}
          placeholder="Exercise"
        />
      </div>

      <div>
        <label className="mb-1 block text-sm font-medium text-slate-700" htmlFor="habit-description">
          Description
        </label>
        <input
          id="habit-description"
          className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
          value={formState.description}
          onChange={(event) => onChangeField("description", event.target.value)}
          placeholder="30 min movement"
        />
      </div>

      <fieldset>
        <legend className="mb-1 text-sm font-medium text-slate-700">Target days</legend>
        <div className="flex flex-wrap gap-2">
          {DAY_OPTIONS.map((day) => (
            <label key={day.value} className="flex items-center gap-1 rounded-md border border-slate-200 px-2 py-1 text-sm">
              <input
                type="checkbox"
                checked={formState.target_days.includes(day.value)}
                onChange={() => toggleDay(day.value)}
              />
              {day.label}
            </label>
          ))}
        </div>
      </fieldset>

      <label className="flex items-center gap-2 text-sm text-slate-700">
        <input
          type="checkbox"
          checked={formState.is_active}
          onChange={(event) => onChangeField("is_active", event.target.checked)}
        />
        Active habit
      </label>

      {error ? <p className="text-sm text-red-600">{error}</p> : null}

      <div className="flex gap-2">
        <Button disabled={isSubmitting} type="submit">
          {isSubmitting ? "Saving..." : submitLabel}
        </Button>
        {onCancel ? (
          <Button className="bg-slate-500 hover:bg-slate-600" onClick={onCancel} type="button">
            Cancel
          </Button>
        ) : null}
      </div>
    </form>
  );
}
