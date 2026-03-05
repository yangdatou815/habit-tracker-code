import { render, screen } from "@testing-library/react";
import { beforeEach, vi } from "vitest";

import { WeeklyHeatmap } from "../components/WeeklyHeatmap";

const useCompletionsQueryMock = vi.fn();

vi.mock("../hooks/useHabits", () => ({
  useCompletionsQuery: (...args) => useCompletionsQueryMock(...args),
}));

describe("WeeklyHeatmap", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders 7 day columns", () => {
    useCompletionsQueryMock.mockReturnValue({
      isLoading: false,
      data: { completions: [] },
    });

    render(<WeeklyHeatmap habitId={1} />);

    const cells = screen.getAllByTestId(/^heatmap-cell-/);
    expect(cells).toHaveLength(7);
  });

  it("marks done days with green", () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");
    const todayStr = `${year}-${month}-${day}`;

    useCompletionsQueryMock.mockReturnValue({
      isLoading: false,
      data: {
        completions: [{ completed_date: todayStr, status: "done" }],
      },
    });

    render(<WeeklyHeatmap habitId={1} />);

    const todayCell = screen.getByTestId(`heatmap-cell-${todayStr}`);
    expect(todayCell.className).toContain("bg-emerald-500");
  });

  it("shows not-scheduled days as neutral", () => {
    useCompletionsQueryMock.mockReturnValue({
      isLoading: false,
      data: { completions: [] },
    });

    // Pass targetDays that almost certainly won't include all 7 days
    render(<WeeklyHeatmap habitId={1} targetDays={["mon"]} />);

    const cells = screen.getAllByTestId(/^heatmap-cell-/);
    const neutralCells = cells.filter((cell) => cell.className.includes("bg-slate-100"));
    // At least some days should be not-scheduled (slate-100)
    expect(neutralCells.length).toBeGreaterThan(0);
  });

  it("handles loading state gracefully", () => {
    useCompletionsQueryMock.mockReturnValue({
      isLoading: true,
      data: null,
    });

    render(<WeeklyHeatmap habitId={1} />);

    // Should still render 7 cells even while loading
    const cells = screen.getAllByTestId(/^heatmap-cell-/);
    expect(cells).toHaveLength(7);
  });
});
