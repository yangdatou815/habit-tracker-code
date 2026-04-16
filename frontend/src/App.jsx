import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import TodayPage from "./pages/TodayPage";
import ProjectsPage from "./pages/ProjectsPage";

const tabs = [
  { to: "/", label: "打卡", icon: "☯", iconActive: "☯" },
  { to: "/projects", label: "管理", icon: "⚙", iconActive: "⚙" },
];

export default function App() {
  return (
    <BrowserRouter>
      <div className="pb-20">
        <Routes>
          <Route path="/" element={<TodayPage />} />
          <Route path="/projects" element={<ProjectsPage />} />
        </Routes>
      </div>

      {/* iOS-style bottom tab bar */}
      <nav className="ios-tabbar fixed bottom-0 left-0 right-0 z-50" style={{ paddingBottom: 'env(safe-area-inset-bottom)' }}>
        <div className="max-w-lg mx-auto flex">
          {tabs.map(({ to, label, icon, iconActive }) => (
            <NavLink
              key={to}
              to={to}
              end={to === "/"}
              className={({ isActive }) =>
                `flex-1 flex flex-col items-center pt-2 pb-1 transition-colors ${
                  isActive ? "text-[#d4b07a]" : "text-[#7a7060]"
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <span className="text-xl leading-none mb-0.5">
                    {isActive ? iconActive : icon}
                  </span>
                  <span className="text-[10px] font-medium">{label}</span>
                </>
              )}
            </NavLink>
          ))}
        </div>
      </nav>
    </BrowserRouter>
  );
}
