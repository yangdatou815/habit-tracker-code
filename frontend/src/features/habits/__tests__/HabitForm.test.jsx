import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";

import { HabitForm } from "../components/HabitForm";

describe("HabitForm", () => {
  it("validates required name", async () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);

    render(<HabitForm onSubmit={onSubmit} />);

    fireEvent.click(screen.getByRole("button", { name: /save habit/i }));

    expect(await screen.findByText(/habit name is required/i)).toBeInTheDocument();
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("submits normalized payload", async () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);

    render(<HabitForm onSubmit={onSubmit} submitLabel="Create habit" />);

    fireEvent.change(screen.getByLabelText(/habit name/i), {
      target: { value: "  Exercise  " },
    });
    fireEvent.change(screen.getByLabelText(/description/i), {
      target: { value: "  30 min movement  " },
    });
    fireEvent.click(screen.getByLabelText("Mon"));
    fireEvent.click(screen.getByRole("button", { name: /create habit/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        name: "Exercise",
        description: "30 min movement",
        target_days: ["mon"],
        is_active: true,
      });
    });

    await waitFor(() => {
      expect(screen.getByLabelText(/habit name/i)).toHaveValue("");
    });
  });
});
