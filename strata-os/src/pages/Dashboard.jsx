import TopBar from "../components/TopBar";
import AiCore from "../components/AiCore";
import StatsGrid from "../components/StatsGrid";

export default function Dashboard() {
  return (
    <div className="dashboard-page">
      <TopBar />

      <div className="dashboard-content">
        <StatsGrid />

        <AiCore />
      </div>
    </div>
  );
}