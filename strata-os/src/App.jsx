import "./App.css";
import { Routes, Route } from "react-router-dom";

import Sidebar from "./components/Sidebar";
import ChatPanel from "./components/ChatPanel";
import StatsPanel from "./components/StatsPanel";
import ControlPanel from "./components/ControlPanel";

import Dashboard from "./pages/Dashboard";
import Leads from "./pages/Leads";
import CRM from "./pages/CRM";
import Calls from "./pages/Calls";
import Analytics from "./pages/Analytics";
import Websites from "./pages/Websites";
import Settings from "./pages/Settings";

function App() {
  return (
    <div className="app">

      <Sidebar />

      <main className="main">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/leads" element={<Leads />} />
          <Route path="/crm" element={<CRM />} />
          <Route path="/calls" element={<Calls />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/websites" element={<Websites />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>

      <aside className="panel">
        <ChatPanel />
        <StatsPanel />
        <ControlPanel />
      </aside>

    </div>
  );
}

export default App;