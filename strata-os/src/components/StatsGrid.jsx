const stats = [
  { title: "Today's Leads", value: "528" },
  { title: "Lead Generator", value: "ACTIVE" },
  { title: "Monday CRM", value: "CONNECTED" },
  { title: "System Status", value: "ONLINE" },
];

function StatsGrid() {
  return (
    <div className="stats-grid">
      {stats.map((stat) => (
        <div className="stat-card" key={stat.title}>
          <div className="stat-title">{stat.title}</div>
          <div className="stat-value">{stat.value}</div>
        </div>
      ))}
    </div>
  );
}

export default StatsGrid;