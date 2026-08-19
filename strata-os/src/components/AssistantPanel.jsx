export default function AssistantPanel() {
  return (
    <div className="assistant-panel">

      <h2>🤖 STRATA AI</h2>

      <div className="card">
        <h4>System Status</h4>
        <p>🟢 Lead Generator</p>
        <p>🟢 Monday CRM</p>
        <p>🟡 Aircall</p>
      </div>

      <div className="card">
        <h4>Today's Stats</h4>
        <p>Leads: 528</p>
        <p>Appointments: 0</p>
        <p>Pipeline: $0</p>
      </div>

      <div className="card">
        <h4>Next Action</h4>
        <button>Generate Leads</button>
      </div>

    </div>
  );
}