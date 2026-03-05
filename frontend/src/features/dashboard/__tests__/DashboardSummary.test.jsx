import { render, screen } from "@testing-library/react";
import { vi } from "vitest";

import { DashboardSummary } from "../components/DashboardSummary";

const useStatsOverviewQueryMock = vi.fn();

vi.mock("../hooks/useStats", () => ({
  useStatsOverviewQuery: (...args) => useStatsOverviewQueryMock(...args),
}));

describe("DashboardSummary", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders loading state", () => {
    useStatsOverviewQueryMock.mockReturnValue({ isLoading: true, data: null, isError: false });

    render(<DashboardSummary />);

    expect(screen.getByText(/Loading stats/i)).toBeInTheDocument();
  });

  it("renders stats data", () => {
    useStatsOverviewQueryMock.mockReturnValue({
      isLoading: false,
      isError: false,
      data: {
        completed_today: 3,
        total_today: 5,
        completion_rate: 82.5,
        total_habits: 6,
      },
    });

    render(<DashboardSummary />);

    expect(screen.getByText("3")).toBeInTheDocument();
    expect(screen.getByText("/5")).toBeInTheDocument();
    expect(screen.getByText("82.5%")).toBeInTheDocument();
    expect(screen.getByText("6")).toBeInTheDocument();
  });

  it("renders nothing on error", () => {
    useStatsOverviewQueryMock.mockReturnValue({ isLoading: false, isError: true, data: null });

    const { container } = render(<DashboardSummary />);

    expect(container.innerHTML).toBe("");
  });
});
