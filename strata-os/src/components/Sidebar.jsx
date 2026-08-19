import { NavLink } from "react-router-dom";
import {
  FiHome,
  FiTarget,
  FiUsers,
  FiPhone,
  FiBarChart2,
  FiGlobe,
  FiMonitor,
  FiSettings,
} from "react-icons/fi";

const links = [
  { to: "/", label: "Dashboard", icon: <FiHome /> },
  { to: "/leads", label: "Lead Generator", icon: <FiTarget /> },
  { to: "/crm", label: "CRM", icon: <FiUsers /> },
  { to: "/calls", label: "Calls", icon: <FiPhone /> },
  { to: "/analytics", label: "Analytics", icon: <FiBarChart2 /> },
  { to: "/browser", label: "Browser", icon: <FiMonitor /> },
  { to: "/websites", label: "Websites", icon: <FiGlobe /> },
  { to: "/settings", label: "Settings", icon: <FiSettings /> },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">

      <div className="sidebar-header">
        <h1>STRATA OS</h1>

        <div className="system-status">
          <span className="status-dot"></span>
          <span>AI CORE ONLINE</span>
        </div>
      </div>

      <nav>
        {links.map((link) => (
          <NavLink
            key={link.label}
            to={link.to}
            className={({ isActive }) =>
              isActive ? "nav-btn active" : "nav-btn"
            }
          >
            {link.icon}
            <span>{link.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <small>STRATA AI v1.0</small>
      </div>

    </aside>
  );
}