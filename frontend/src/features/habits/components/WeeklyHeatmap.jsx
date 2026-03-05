import { useCompletionsQuery } from "../hooks/useHabits";
import { formatLocalDate } from "./CompletionToggle";

const DAY_NAME_MAP = { Mon: "mon", Tue: "tue", Wed: "wed", Thu: "thu", Fri: "fri", Sat: "sat", Sun: "sun" };

function getLast7Days() {
  const days = [];
  const today = new Date();
  for (let i = 6; i >= 0; i--) {
    const d = new Date(today);
    d.setDate(today.getDate() - i);
    days.push(d);
  }
  return days;
}

function getDayAbbrev(dateObj) {
  return dateObj.toLocaleDateString("en-US", { weekday: "short" }).slice(0, 2);
}

export function WeeklyHeatmap({ habitId, targetDays = [] }) {
  const days = getLast7Days();
  const fromDate = formatLocalDate(days[0]);
  const toDate = formatLocalDate(days[6]);
  const completionsQuery = useCompletionsQuery(habitId, { from: fromDate, to: toDate });

  const completionMap = {};
  (completionsQuery.data?.completions || []).forEach((c) => {
    completionMap[c.completed_date] = c.status;
  });

  return (
    <div className="flex gap-1" role="group" aria-label="Weekly completion heatmap">
      {days.map((dayDate) => {
        const dateStr = formatLocalDate(dayDate);
        const status = completionMap[dateStr];
        const dayAbbrev = dayDate.toLocaleDateString("en-US", { weekday: "short" });
        const isScheduled = targetDays.length === 0 || targetDays.includes(DAY_NAME_MAP[dayAbbrev]);

        let bgColor = "bg-slate-100";
        if (isScheduled) {
          if (status === "done") bgColor = "bg-emerald-500";
          else if (status === "not_done") bgColor = "bg-red-300";
          else bgColor = "bg-slate-200";
        }

        return (
          <div key={dateStr} className="flex flex-col items-center gap-0.5" title={dateStr}>
            <span className="text-[10px] text-slate-500">{getDayAbbrev(dayDate)}</span>
            <div className={`h-5 w-5 rounded-sm ${bgColor}`} data-testid={`heatmap-cell-${dateStr}`} />
          </div>
        );
      })}
    </div>
  );
}
