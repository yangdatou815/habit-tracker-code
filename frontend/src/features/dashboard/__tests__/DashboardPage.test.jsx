import { render, screen } from "@testing-library/react";
import { vi } from "vitest";

import { DashboardPage } from "../components/DashboardPage";

vi.mock("../../habits", () => ({
  HabitForm: () => <div>Habit form</div>,
  HabitList: () => <div>Habit list</div>,
  useCreateHabitMutation: () => ({ mutateAsync: vi.fn() }),
}));

vi.mock("../components/DashboardSummary", () => ({
  DashboardSummary: () => <div>Dashboard summary</div>,
}));

describe("DashboardPage", () => {
  it("renders dashboard heading", () => {
    render(<DashboardPage />);

    expect(screen.getByText(/Habit Tracker Dashboard/i)).toBeInTheDocument();
    expect(screen.getByText(/Dashboard summary/i)).toBeInTheDocument();
    expect(screen.getByText(/Add habit/i)).toBeInTheDocument();
    expect(screen.getByText(/Habit form/i)).toBeInTheDocument();
    expect(screen.getByText(/Habit list/i)).toBeInTheDocument();
  });
});
