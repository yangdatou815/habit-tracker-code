import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  createHabit,
  deleteHabit,
  fetchHabit,
  fetchHabitCompletions,
  fetchHabits,
  updateHabit,
  upsertHabitCompletion,
} from "../api/habits";

export const habitQueryKeys = {
  all: ["habits"],
  list: (isActive = "all") => ["habits", "list", isActive],
  detail: (habitId) => ["habits", "detail", habitId],
  completions: (habitId, from = "all", to = "all") => ["habits", "completions", habitId, from, to],
};

export function useHabitsQuery({ isActive } = {}) {
  const queryKeyValue = isActive === undefined ? "all" : String(isActive);

  return useQuery({
    queryKey: habitQueryKeys.list(queryKeyValue),
    queryFn: () => fetchHabits({ isActive }),
  });
}

export function useHabitDetailQuery(habitId) {
  return useQuery({
    queryKey: habitQueryKeys.detail(habitId),
    queryFn: () => fetchHabit(habitId),
    enabled: typeof habitId === "number",
  });
}

export function useCompletionsQuery(habitId, { from, to } = {}) {
  return useQuery({
    queryKey: habitQueryKeys.completions(habitId, from, to),
    queryFn: () => fetchHabitCompletions(habitId, { from, to }),
    enabled: typeof habitId === "number",
  });
}

export function useCreateHabitMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createHabit,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: habitQueryKeys.all });
    },
  });
}

export function useUpdateHabitMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ habitId, payload }) => updateHabit(habitId, payload),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: habitQueryKeys.all });
      queryClient.invalidateQueries({ queryKey: habitQueryKeys.detail(variables.habitId) });
    },
  });
}

export function useDeleteHabitMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteHabit,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: habitQueryKeys.all });
    },
  });
}

export function useUpsertCompletionMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ habitId, completedDate, status }) => upsertHabitCompletion(habitId, completedDate, status),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: habitQueryKeys.all });
      queryClient.invalidateQueries({
        queryKey: habitQueryKeys.completions(variables.habitId, variables.completedDate, variables.completedDate),
      });
      queryClient.invalidateQueries({ queryKey: habitQueryKeys.detail(variables.habitId) });
    },
  });
}
