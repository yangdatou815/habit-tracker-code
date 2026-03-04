import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, vi } from "vitest";

import { HabitList } from "../components/HabitList";

const useHabitsQueryMock = vi.fn();

vi.mock("../hooks/useHabits", () => ({
  useHabitsQuery: (...args) => useHabitsQueryMock(...args),
}));

vi.mock("../components/HabitCard", () => ({
  HabitCard: ({ habit }) => <div>{habit.name}</div>,
}));

describe("HabitList", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders loading state", () => {
    useHabitsQueryMock.mockReturnValue({
      isLoading: true,
      isError: false,
      data: [],
    });

    render(<HabitList />);

    expect(screen.getByText(/loading habits/i)).toBeInTheDocument();
  });

  it("renders empty state", () => {
    useHabitsQueryMock.mockReturnValue({
      isLoading: false,
      isError: false,
      data: [],
    });

    render(<HabitList />);

    expect(screen.getByText(/no habits yet/i)).toBeInTheDocument();
  });

  it("renders habits and toggles archived filter", () => {
    useHabitsQueryMock.mockReturnValue({
      isLoading: false,
      isError: false,
      data: [{ id: 1, name: "Exercise" }],
    });

    render(<HabitList />);

    expect(screen.getByText("Exercise")).toBeInTheDocument();
    fireEvent.click(screen.getByLabelText(/show archived/i));
    expect(useHabitsQueryMock).toHaveBeenLastCalledWith({ isActive: undefined });
  });
});
