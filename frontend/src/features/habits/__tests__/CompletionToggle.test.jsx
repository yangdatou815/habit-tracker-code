import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, vi } from "vitest";

import { CompletionToggle, formatLocalDate } from "../components/CompletionToggle";

const useCompletionsQueryMock = vi.fn();
const useUpsertCompletionMutationMock = vi.fn();

vi.mock("../hooks/useHabits", () => ({
  useCompletionsQuery: (...args) => useCompletionsQueryMock(...args),
  useUpsertCompletionMutation: (...args) => useUpsertCompletionMutationMock(...args),
}));

describe("CompletionToggle", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows done state and toggles to not_done", async () => {
    const mutateAsync = vi.fn().mockResolvedValue(undefined);

    useCompletionsQueryMock.mockReturnValue({
      isLoading: false,
      data: {
        completions: [{ id: 1, habit_id: 1, completed_date: "2026-03-04", status: "done" }],
      },
    });
    useUpsertCompletionMutationMock.mockReturnValue({ isPending: false, mutateAsync });

    render(<CompletionToggle habitId={1} />);

    fireEvent.click(screen.getByRole("button", { name: /marked done/i }));

    expect(mutateAsync).toHaveBeenCalledWith(
      expect.objectContaining({
        habitId: 1,
        status: "not_done",
      }),
    );
  });

  it("shows not-done state when no completion exists", () => {
    useCompletionsQueryMock.mockReturnValue({
      isLoading: false,
      data: { completions: [] },
    });
    useUpsertCompletionMutationMock.mockReturnValue({
      isPending: false,
      mutateAsync: vi.fn().mockResolvedValue(undefined),
    });

    render(<CompletionToggle habitId={1} />);

    expect(screen.getByRole("button", { name: /mark done/i })).toBeInTheDocument();
  });

  it("formats local date parts rather than UTC ISO slice", () => {
    const fakeDate = {
      getFullYear: () => 2026,
      getMonth: () => 2,
      getDate: () => 5,
      toISOString: () => "2026-03-04T16:30:00.000Z",
    };

    expect(formatLocalDate(fakeDate)).toBe("2026-03-05");
  });
});
