import { render, screen } from "@testing-library/react";

import { HabitListPlaceholder } from "../components/HabitListPlaceholder";

describe("HabitListPlaceholder", () => {
  it("renders placeholder text", () => {
    render(<HabitListPlaceholder />);

    expect(screen.getByText("Habits")).toBeInTheDocument();
    expect(screen.getByText(/No habits yet/i)).toBeInTheDocument();
  });
});
