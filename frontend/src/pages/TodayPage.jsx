import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getDateCheckins, getHistory, toggleCheckin } from "../features/projects/api";

const CATEGORY_ICONS = {
  "静功": "🧘",
  "柔韧": "🤸",
  "动功": "💪",
  "养生": "🌿",
  "其他": "📌",
};

function formatDate(d) {
  return d.toISOString().slice(0, 10);
}

function getDateRange(days) {
  const to = new Date();
  const from = new Date();
  from.setDate(from.getDate() - days + 1);
  return { from: formatDate(from), to: formatDate(to) };
}

function shortDate(dateStr) {
  const [, m, d] = dateStr.split("-");
  return parseInt(m) + "/" + parseInt(d);
}

function pctColor(pct) {
  if (pct === 100) return "bg-[#6ab584]";
  if (pct >= 80) return "bg-[#5aa572]";
  if (pct >= 60) return "bg-[#d4b07a]";
  if (pct >= 40) return "bg-[#b8904a]";
  if (pct > 0) return "bg-[#9a5a48]";
  return "bg-[#353545]";
}

function groupByCategory(items) {
  const groups = {};
  for (const item of items) {
    if (!groups[item.category]) groups[item.category] = [];
    groups[item.category].push(item);
  }
  return groups;
}

export default function TodayPage() {
  const today = formatDate(new Date());
  const [selectedDate, setSelectedDate] = useState(today);
  const queryClient = useQueryClient();
  const range = getDateRange(30);

  const { data: history, isLoading: histLoading } = useQuery({
    queryKey: ["checkins", "history", range.from, range.to],
    queryFn: () => getHistory(range.from, range.to),
  });

  const { data: dayDetail, isLoading: dayLoading } = useQuery({
    queryKey: ["checkins", "date", selectedDate],
    queryFn: () => getDateCheckins(selectedDate),
    enabled: !!selectedDate,
  });

  const mutation = useMutation({
    mutationFn: ({ projectId, date, status }) =>
      toggleCheckin(projectId, date, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["checkins"] });
    },
  });

  const handleToggle = (item) => {
    const newStatus = item.status === "done" ? "not_done" : "done";
    mutation.mutate({ projectId: item.project_id, date: selectedDate, status: newStatus });
  };

  const isToday = selectedDate === today;

  return (
    <div className="max-w-5xl mx-auto px-4 pt-2 relative overflow-hidden">

      {/* Floating cloud decorations */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <svg className="dao-float-1 absolute top-16 left-[5%] w-40 h-20" viewBox="0 0 160 80" fill="none">
          <path d="M20 60 Q40 30 70 45 Q90 20 120 35 Q140 25 150 40 Q155 50 140 55 Q130 60 100 55 Q80 50 60 58 Q40 65 20 60Z" fill="#d4b07a" fillOpacity="0.06"/>
        </svg>
        <svg className="dao-float-2 absolute top-40 right-[8%] w-32 h-16" viewBox="0 0 130 60" fill="none">
          <path d="M15 45 Q30 20 55 32 Q75 15 100 28 Q115 22 120 35 Q125 45 110 48 Q90 50 70 46 Q50 42 30 48Z" fill="#d4b07a" fillOpacity="0.05"/>
        </svg>
        <svg className="dao-float-3 absolute bottom-32 left-[15%] w-36 h-18" viewBox="0 0 144 72" fill="none">
          <path d="M18 54 Q36 24 63 38 Q81 16 108 30 Q126 22 135 36 Q140 46 126 49 Q108 52 81 48 Q63 44 36 52Z" fill="#d4b07a" fillOpacity="0.04"/>
        </svg>
      </div>

      {/* Header with Yin-Yang */}
      <div className="pt-2 pb-3 flex items-center gap-4">
        <svg className="dao-yinyang-spin w-12 h-12 flex-shrink-0" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="48" fill="none" stroke="#d4b07a" strokeWidth="1.5" strokeOpacity="0.3"/>
          <path d="M50 2 A48 48 0 0 1 50 98 A24 24 0 0 1 50 50 A24 24 0 0 0 50 2Z" fill="#d4b07a" fillOpacity="0.15"/>
          <path d="M50 2 A48 48 0 0 0 50 98 A24 24 0 0 0 50 50 A24 24 0 0 1 50 2Z" fill="#6ab584" fillOpacity="0.12"/>
          <circle cx="50" cy="26" r="6" fill="#6ab584" fillOpacity="0.2"/>
          <circle cx="50" cy="74" r="6" fill="#d4b07a" fillOpacity="0.25"/>
        </svg>
        <div>
          <h1 className="text-[34px] font-bold tracking-tight text-[#ece5d6]">
            {isToday ? "今日打卡" : selectedDate}
          </h1>
          {!isToday && (
            <button
              onClick={() => setSelectedDate(today)}
              className="text-[15px] text-[#d4b07a] font-normal mt-1"
            >
              ← 回到今天
            </button>
          )}
        </div>
      </div>

      {/* Cloud divider */}
      <div className="dao-cloud-divider mb-3"></div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">

        {/* ── Left Column: Checkin Detail ── */}
        <div>
          {dayLoading && (
            <div className="text-center text-[#9a9080] py-12 text-[15px]">加载中...</div>
          )}
          {dayDetail && (() => {
            const pct = dayDetail.total > 0
              ? Math.round((dayDetail.done_count / dayDetail.total) * 100)
              : 0;
            const grouped = groupByCategory(dayDetail.items);
            return (
              <>
                {/* Progress card with corner ornaments */}
                <div className="ios-card dao-ornament p-4 mb-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-[13px] font-semibold text-[#9a9080] uppercase tracking-wide">
                      完成进度
                    </span>
                    <div className="flex items-center gap-2">
                      {pct === 100 && (
                        <span className="dao-seal text-[11px] text-[#6ab584] border-[#6ab584]">
                          圆满
                        </span>
                      )}
                      <span className="text-[15px] font-semibold text-[#ece5d6]">
                        {dayDetail.done_count}/{dayDetail.total}
                      </span>
                    </div>
                  </div>
                  <div className="ios-progress">
                    <div
                      className="ios-progress-fill"
                      style={{
                        width: pct + "%",
                        backgroundColor: pct === 100 ? "#6ab584" : pct >= 60 ? "#d4b07a" : "#9a8455",
                      }}
                    />
                  </div>
                  <div className="text-right mt-1">
                    <span className="text-[13px] font-medium" style={{
                      color: pct === 100 ? "#6ab584" : pct >= 60 ? "#d4b07a" : "#9a8455",
                    }}>
                      {pct}%
                    </span>
                  </div>
                </div>

                {/* Checkin items - iOS grouped list style */}
                {Object.entries(grouped).map(([category, catItems]) => (
                  <div key={category} className="mb-4">
                    <div className="px-4 pb-1.5 flex items-center gap-2">
                      <span className="h-px flex-1 max-w-4 bg-[#d4b07a]/20"></span>
                      <span className="text-[13px] font-semibold text-[#d4b07a] uppercase tracking-wide">
                        {CATEGORY_ICONS[category] || "📌"} {category}
                      </span>
                      <span className="h-px flex-1 max-w-4 bg-[#d4b07a]/20"></span>
                    </div>
                    <div className="ios-section">
                      {catItems.map((item, idx) => (
                        <button
                          key={item.project_id}
                          onClick={() => handleToggle(item)}
                          disabled={mutation.isPending}
                          className={
                            "w-full flex items-center justify-between px-4 py-3 active:bg-white/5 transition-colors " +
                            (idx < catItems.length - 1 ? "border-b border-[#d4b07a]/10" : "")
                          }
                        >
                          <span className={
                            "text-[17px] " +
                            (item.status === "done"
                              ? "text-[#7a7060] line-through"
                              : "text-[#ece5d6]")
                          }>
                            {item.project_name}
                          </span>
                          <div
                            className={
                              "ios-switch " +
                              (item.status === "done" ? "ios-switch-on" : "ios-switch-off")
                            }
                          />
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </>
            );
          })()}
        </div>

        {/* ── Right Column: History Calendar ── */}
        <div>
          <div className="px-4 pb-2 flex items-center gap-2">
            <svg className="w-5 h-5 flex-shrink-0" viewBox="0 0 24 24" fill="none">
              <path d="M12 1L22 6.5V17.5L12 23L2 17.5V6.5L12 1Z" stroke="#d4b07a" strokeWidth="1" strokeOpacity="0.4"/>
              <path d="M12 5L18 8.5V15.5L12 19L6 15.5V8.5L12 5Z" stroke="#d4b07a" strokeWidth="0.6" strokeOpacity="0.3"/>
            </svg>
            <span className="text-[13px] font-semibold text-[#d4b07a] uppercase tracking-wide">
              历史记录
            </span>
          </div>

          {histLoading ? (
            <div className="text-[#9a9080] text-[15px] py-12 text-center">加载中...</div>
          ) : (
            <div className="ios-card dao-ornament p-3">
              <div className="grid grid-cols-7 gap-1">
                {/* Weekday headers */}
                {["一", "二", "三", "四", "五", "六", "日"].map((d) => (
                  <div key={d} className="text-center text-[11px] text-[#9a9080] font-medium pb-1">
                    {d}
                  </div>
                ))}

                {/* Calendar cells */}
                {(() => {
                  const days = (history || []).slice().reverse();
                  if (days.length === 0) return null;
                  const firstDate = new Date(days[0].date + "T00:00:00");
                  const startDow = (firstDate.getDay() + 6) % 7;
                  const empties = [];
                  for (let i = 0; i < startDow; i++) {
                    empties.push(<div key={"e" + i} />);
                  }
                  return [
                    ...empties,
                    ...days.map((day) => {
                      const pct = day.total > 0
                        ? Math.round((day.done_count / day.total) * 100)
                        : 0;
                      const isSelected = selectedDate === day.date;
                      const isDayToday = day.date === today;
                      return (
                        <button
                          key={day.date}
                          onClick={() => setSelectedDate(day.date)}
                          className={
                            "flex flex-col items-center py-1 rounded-xl transition-all " +
                            (isSelected
                              ? "bg-[#d4b07a]/15 ring-1.5 ring-[#d4b07a]"
                              : "active:bg-white/5")
                          }
                          title={day.date + ": " + day.done_count + "/" + day.total}
                        >
                          <div className={
                            "w-7 h-7 rounded-full flex items-center justify-center text-white font-semibold text-[11px] " +
                            pctColor(pct)
                          }>
                            {day.done_count}
                          </div>
                          <span className={
                            "text-[10px] mt-0.5 " +
                            (isDayToday
                              ? "font-bold text-[#d4b07a]"
                              : "text-[#9a9080]")
                          }>
                            {shortDate(day.date)}
                          </span>
                        </button>
                      );
                    }),
                  ];
                })()}
              </div>

              {/* Legend */}
              <div className="flex items-center justify-center gap-2.5 mt-3 pt-3 border-t border-[#d4b07a]/10">
                {[
                  { color: "bg-[#6ab584]", label: "全部" },
                  { color: "bg-[#d4b07a]", label: "大部分" },
                  { color: "bg-[#b8904a]", label: "部分" },
                  { color: "bg-[#9a5a48]", label: "少量" },
                  { color: "bg-[#353545]", label: "无" },
                ].map(({ color, label }) => (
                  <span key={label} className="flex items-center gap-1 text-[11px] text-[#9a9080]">
                    <span className={"w-2.5 h-2.5 rounded-full inline-block " + color} />
                    {label}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Selected date summary */}
          {dayDetail && !isToday && (
            <div className="ios-card p-4 mt-3">
              <div className="text-[13px] font-semibold text-[#9a9080] mb-2">
                {selectedDate} · {dayDetail.done_count}/{dayDetail.total} 已完成
              </div>
              <div className="flex flex-wrap gap-1.5">
                {dayDetail.items.map((item) => (
                  <span
                    key={item.project_id}
                    className={
                      "inline-flex items-center gap-1 text-[13px] px-2.5 py-1 rounded-full " +
                      (item.status === "done"
                        ? "bg-[#6ab584]/20 text-[#8ed4a8]"
                        : "bg-[#353545] text-[#9a9080]")
                    }
                  >
                    {item.status === "done" ? "✓" : "·"} {item.project_name}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
