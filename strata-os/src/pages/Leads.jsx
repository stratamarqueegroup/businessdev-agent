export default function Leads() {
  const leads = [
    {
      company: "ABC Roofing",
      industry: "Construction",
      location: "Miami, FL",
      score: 94,
      status: "NEW",
    },
    {
      company: "Miami Dental Group",
      industry: "Dental",
      location: "Miami, FL",
      score: 87,
      status: "CONTACTED",
    },
    {
      company: "Sunset Hotels",
      industry: "Hospitality",
      location: "Orlando, FL",
      score: 81,
      status: "QUALIFIED",
    },
  ];

  return (
    <div style={{ padding: "30px" }}>
      <div style={{ marginBottom: "30px" }}>
        <h1>Leads</h1>
        <p>Manage and qualify your business prospects.</p>
      </div>

      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Search leads..."
          style={{
            width: "100%",
            maxWidth: "500px",
            padding: "12px",
          }}
        />
      </div>

      <div>
        {leads.map((lead) => (
          <div
            key={lead.company}
            style={{
              padding: "20px",
              marginBottom: "12px",
              border: "1px solid #333",
              borderRadius: "10px",
            }}
          >
            <h3>{lead.company}</h3>
            <p>{lead.industry}</p>
            <p>{lead.location}</p>
            <p>Lead Score: {lead.score}</p>
            <strong>{lead.status}</strong>
          </div>
        ))}
      </div>
    </div>
  );
}