import { render, screen } from "@testing-library/react";

import { DashboardPage } from "../components/DashboardPage";

describe("DashboardPage", () => {
  it("renders dashboard heading", () => {
    render(<DashboardPage />);

    expect(screen.getByText(/Habit Tracker Dashboard/i)).toBeInTheDocument();
    expect(screen.getByText(/Foundation scaffold complete/i)).toBeInTheDocument();
  });
});
