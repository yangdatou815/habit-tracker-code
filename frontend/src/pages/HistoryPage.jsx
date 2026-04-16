import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getDateCheckins, toggleCheckin } from "../features/projects/api";

const CATEGORY_COLORS = {
  静功: "bg-purple-100 text-purple-700",
  柔韧: "bg-blue-100 text-blue-700",
  动功: "bg-green-100 text-green-700",
  养生: "bg-orange-100 text-orange-700",
  其他: "bg-gray-100 text-gray-700",
};

function formatDate(d) {
  return d.toISOString().slice(0, 10);
}

function groupByCategory(items) {
  const groups = {};
  for (const item of items) {
    if (!groups[item.category]) groups[item.category] = [];
    groups[item.category].push(item);
  }
  return groups;
}

export default function HistoryPage() {
  const [selectedDate, setSelectedDate] = useState(formatDate(new Date()));
  const queryClient = useQueryClient();

  const { data, isLoading, error } = useQuery({
    queryKey: ["checkins", "date", selectedDate],
    queryFn: () => getDateCheckins(selectedDate),
    enabled: !!selectedDate,
  });

  const mutation = useMutation({
    mutationFn: ({ projectId, date, status }) =>
      toggleCheckin(projectId, date, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["checkins", "date", selectedDate] });
    },
  });

  const handleToggle = (item) => {
    const newStatus = item.status === "done" ? "not_done" : "done";
    mutation.mutate({ projectId: item.project_id, date: selectedDate, status: newStatus });
  };

  return (
    <div className="max-w-lg mx-auto p-4">
      <h1 className="text-xl font-bold mb-4">历史记录</h1>

      <input
        type="date"
        value={selectedDate}
        onChange={(e) => setSelectedDate(e.target.value)}
        className="w-full mb-4 p-2 border border-gray-300 rounded-lg"
      />

      {isLoading && <div className="text-center text-gray-500">加载中...</div>}
      {error && <div className="text-center text-red-500">加载失败</div>}

      {data && (
        <>
          <div className="flex justify-between items-center mb-4">
            <span className="text-sm text-gray-600">{data.date}</span>
            <span className="text-sm font-medium text-gray-600">
              {data.done_count}/{data.total} 已完成
            </span>
          </div>

          {Object.entries(groupByCategory(data.items)).map(([category, catItems]) => (
            <div key={category} className="mb-4">
              <h2 className="text-sm font-semibold text-gray-500 mb-2">{category}</h2>
              <div className="space-y-2">
                {catItems.map((item) => (
                  <button
                    key={item.project_id}
                    onClick={() => handleToggle(item)}
                    disabled={mutation.isPending}
                    className={`w-full flex items-center justify-between p-3 rounded-lg border-2 transition-all ${
                      item.status === "done"
                        ? "border-green-400 bg-green-50"
                        : "border-gray-200 bg-white hover:border-gray-300"
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">
                        {item.status === "done" ? "✅" : "⬜"}
                      </span>
                      <span className={`font-medium ${item.status === "done" ? "text-green-700" : "text-gray-800"}`}>
                        {item.project_name}
                      </span>
                    </div>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${CATEGORY_COLORS[item.category] || CATEGORY_COLORS["其他"]}`}>
                      {item.category}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </>
      )}
    </div>
  );
}
