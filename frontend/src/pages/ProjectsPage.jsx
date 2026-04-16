import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  listProjects,
  createProject,
  updateProject,
  deleteProject,
} from "../features/projects/api";

const CATEGORIES = ["静功", "柔韧", "动功", "养生", "其他"];

export default function ProjectsPage() {
  const queryClient = useQueryClient();
  const [newName, setNewName] = useState("");
  const [newCategory, setNewCategory] = useState("其他");
  const [editingId, setEditingId] = useState(null);
  const [editName, setEditName] = useState("");
  const [editCategory, setEditCategory] = useState("");

  const { data: projects, isLoading } = useQuery({
    queryKey: ["projects"],
    queryFn: () => listProjects(),
  });

  const createMut = useMutation({
    mutationFn: (data) => createProject(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["projects"] });
      setNewName("");
      setNewCategory("其他");
    },
  });

  const updateMut = useMutation({
    mutationFn: ({ id, data }) => updateProject(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["projects"] });
      setEditingId(null);
    },
  });

  const deleteMut = useMutation({
    mutationFn: (id) => deleteProject(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["projects"] }),
  });

  const handleCreate = (e) => {
    e.preventDefault();
    if (!newName.trim()) return;
    createMut.mutate({ name: newName.trim(), category: newCategory });
  };

  const startEdit = (p) => {
    setEditingId(p.id);
    setEditName(p.name);
    setEditCategory(p.category);
  };

  const saveEdit = (id) => {
    updateMut.mutate({ id, data: { name: editName, category: editCategory } });
  };

  return (
    <div className="max-w-lg mx-auto px-4 pt-2">

      {/* iOS large title */}
      <div className="pt-2 pb-3">
        <h1 className="text-[34px] font-bold tracking-tight text-[#ece5d6]">
          项目管理
        </h1>
      </div>

      {/* Add form - iOS style */}
      <div className="ios-section mb-6">
        <form onSubmit={handleCreate}>
          <div className="px-4 py-3 border-b border-[#d4b07a]/10">
            <input
              type="text"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              placeholder="新项目名称"
              className="w-full text-[17px] text-[#ece5d6] placeholder-[#7a7060] bg-transparent outline-none"
            />
          </div>
          <div className="flex items-center justify-between px-4 py-3">
            <select
              value={newCategory}
              onChange={(e) => setNewCategory(e.target.value)}
              className="text-[15px] text-[#9a9080] bg-transparent outline-none"
            >
              {CATEGORIES.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
            <button
              type="submit"
              disabled={createMut.isPending || !newName.trim()}
              className="px-5 py-1.5 dao-gold-bg text-[#1a1408] text-[15px] font-semibold rounded-full disabled:opacity-40 active:opacity-70 transition-opacity"
            >
              添加
            </button>
          </div>
        </form>
      </div>

      {isLoading && (
        <div className="text-center text-[#9a9080] text-[15px] py-8">加载中...</div>
      )}

      {/* Project list - iOS grouped table */}
      <div className="px-4 pb-1.5">
        <span className="text-[13px] font-semibold text-[#d4b07a] uppercase tracking-wide">
          全部项目
        </span>
      </div>
      <div className="ios-section">
        {projects?.map((p, idx) => (
          <div
            key={p.id}
            className={
              "px-4 py-3 " +
              (idx < projects.length - 1 ? "border-b border-[#d4b07a]/10" : "") +
              (!p.is_active ? " opacity-50" : "")
            }
          >
            {editingId === p.id ? (
              <div>
                <input
                  type="text"
                  value={editName}
                  onChange={(e) => setEditName(e.target.value)}
                  className="w-full text-[17px] text-[#ece5d6] bg-transparent border-b border-[#d4b07a] outline-none mb-2 pb-1"
                />
                <div className="flex items-center justify-between">
                  <select
                    value={editCategory}
                    onChange={(e) => setEditCategory(e.target.value)}
                    className="text-[15px] text-[#9a9080] bg-transparent outline-none"
                  >
                    {CATEGORIES.map((c) => (
                      <option key={c} value={c}>{c}</option>
                    ))}
                  </select>
                  <div className="flex gap-3">
                    <button
                      onClick={() => setEditingId(null)}
                      className="text-[15px] text-[#9a9080]"
                    >
                      取消
                    </button>
                    <button
                      onClick={() => saveEdit(p.id)}
                      className="text-[15px] text-[#d4b07a] font-semibold"
                    >
                      保存
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <span className="text-[17px] text-[#ece5d6]">{p.name}</span>
                  <span className="text-[13px] text-[#9a9080] bg-[#d4b07a]/10 px-2 py-0.5 rounded-full">
                    {p.category}
                  </span>
                </div>
                <div className="flex items-center gap-4">
                  <button
                    onClick={() => startEdit(p)}
                    className="text-[15px] text-[#d4b07a]"
                  >
                    编辑
                  </button>
                  <button
                    onClick={() => {
                      if (window.confirm(`确认删除「${p.name}」？`)) {
                        deleteMut.mutate(p.id);
                      }
                    }}
                    className="text-[15px] text-[#9a5a48]"
                  >
                    删除
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
