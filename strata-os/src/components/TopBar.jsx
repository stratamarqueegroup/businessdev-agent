import { FiSearch, FiBell, FiCpu, FiClock, FiMic } from "react-icons/fi";

export default function TopBar() {
  const time = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <header className="topbar">

      <div className="brand">
        <div className="brand-core"></div>

        <div>
          <h2>STRATA OS</h2>
          <small>Artificial Intelligence Command Center</small>
        </div>
      </div>

      <div className="search-box">
        <FiSearch className="search-icon" />

        <input
          type="text"
          placeholder="Ask STRATA or search anything..."
        />

        <button className="voice-btn">
          <FiMic />
        </button>
      </div>

      <div className="topbar-right">

        <div className="status-pill">
          <FiCpu />
          <span>AI ONLINE</span>
        </div>

        <button className="icon-btn">
          <FiBell />
        </button>

        <div className="clock">
          <FiClock />
          <span>{time}</span>
        </div>

      </div>

    </header>
  );
}