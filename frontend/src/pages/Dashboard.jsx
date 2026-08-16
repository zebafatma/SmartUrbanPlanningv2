import { useEffect, useState } from "react";
import { getUrbanData } from "../services/api";
import "./Dashboard.css";

function Dashboard() {
  const [urbanData, setUrbanData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Temporary values for testing.
  // We'll connect these to the Analysis page next.
  const area = "Indiranagar";
  const ward = "Kempegowda Ward";

  useEffect(() => {
    const loadUrbanData = async () => {
      setLoading(true);
      setError("");

      try {
        const data = await getUrbanData(area, ward);
        setUrbanData(data);
      } catch (err) {
        setError(
          err.message || "Failed to load urban data."
        );
      } finally {
        setLoading(false);
      }
    };

    loadUrbanData();
  }, []);

  return (
    <main className="dashboard-page">

      {/* Header */}

      <section className="dashboard-header">

        <div>
          <span className="section-tag">
            URBAN DASHBOARD
          </span>

          <h1>
            Urban
            <span> Overview</span>
          </h1>

          <p>
            A consolidated view of the selected area's
            environmental and urban conditions.
          </p>
        </div>

        <div className="location-card">

          <span>ANALYSIS AREA</span>

          <strong>{area}</strong>

          <small>{ward}</small>

        </div>

      </section>


      {/* Loading */}

      {loading && (
        <div className="dashboard-state">
          <span className="dashboard-spinner" />
          Loading urban data...
        </div>
      )}


      {/* Error */}

      {error && (
        <div className="dashboard-error">
          {error}
        </div>
      )}


      {/* Dashboard */}

      {!loading && !error && urbanData && (

        <section className="dashboard-content">

          {/* Overview Cards */}

          <div className="metric-grid">

            <MetricCard
              label="Traffic"
              value={
                urbanData.traffic
                  ? "Available"
                  : "N/A"
              }
              icon="↗"
              type="blue"
            />

            <MetricCard
              label="Population"
              value={
                urbanData.population
                  ? "Available"
                  : "N/A"
              }
              icon="◎"
              type="green"
            />

            <MetricCard
              label="Weather"
              value={
                urbanData.weather
                  ? "Available"
                  : "N/A"
              }
              icon="☁"
              type="teal"
            />

            <MetricCard
              label="Accidents"
              value={
                urbanData.accidents
                  ? "Available"
                  : "N/A"
              }
              icon="!"
              type="orange"
            />

          </div>


          {/* Data Sections */}

          <div className="dashboard-grid">

            <DataCard
              title="Traffic Conditions"
              data={urbanData.traffic}
              type="blue"
            />

            <DataCard
              title="Population"
              data={urbanData.population}
              type="green"
            />

            <DataCard
              title="Weather"
              data={urbanData.weather}
              type="teal"
            />

            <DataCard
              title="Road Accidents"
              data={urbanData.accidents}
              type="orange"
            />

          </div>


          {/* Amenities */}

          <section className="amenities-section">

            <div className="section-title-row">

              <div>
                <span className="section-tag">
                  INFRASTRUCTURE
                </span>

                <h2>
                  Urban Amenities
                </h2>
              </div>

            </div>


            <div className="amenities-grid">

              {Object.entries(
                urbanData.amenities || {}
              ).map(([name, value]) => (

                <div
                  className="amenity-card"
                  key={name}
                >

                  <div className="amenity-icon">
                    {getAmenityIcon(name)}
                  </div>

                  <div>
                    <span>{name}</span>

                    <strong>
                      {getAmenityValue(value)}
                    </strong>
                  </div>

                </div>

              ))}

            </div>

          </section>

        </section>

      )}

    </main>
  );
}


/* ==========================================================
   Metric Card
   ========================================================== */

function MetricCard({
  label,
  value,
  icon,
  type,
}) {
  return (
    <div className="metric-card">

      <div className={`metric-icon ${type}`}>
        {icon}
      </div>

      <div>
        <span>{label}</span>

        <strong>{value}</strong>
      </div>

    </div>
  );
}


/* ==========================================================
   Data Card
   ========================================================== */

function DataCard({
  title,
  data,
  type,
}) {
  return (
    <div className="data-card">

      <div className="data-card-header">

        <h3>{title}</h3>

        <span className={`data-indicator ${type}`} />

      </div>

      {data ? (
        <div className="data-values">
          {Object.entries(data)
            .filter(
              ([, value]) =>
                value !== null &&
                value !== undefined &&
                typeof value !== "object"
            )
            .slice(0, 6)
            .map(([key, value]) => (

              <div
                className="data-row"
                key={key}
              >

                <span>
                  {formatLabel(key)}
                </span>

                <strong>
                  {formatValue(value)}
                </strong>

              </div>

            ))}
        </div>
      ) : (
        <p className="no-data">
          No data available.
        </p>
      )}

    </div>
  );
}


/* ==========================================================
   Helpers
   ========================================================== */

function formatLabel(value) {
  return value
    .replaceAll("_", " ")
    .replace(
      /\b\w/g,
      (letter) => letter.toUpperCase()
    );
}


function formatValue(value) {
  if (typeof value === "number") {
    return Number.isInteger(value)
      ? value
      : value.toFixed(2);
  }

  return String(value);
}


function getAmenityIcon(name) {
  const icons = {
    Hospitals: "✚",
    Schools: "◇",
    "Bus Stops": "●",
    Metro: "◆",
    Roads: "━",
    Water: "≈",
    Parks: "✿",
  };

  return icons[name] || "•";
}


function getAmenityValue(value) {
  if (!value) {
    return "Available";
  }

  if (typeof value === "object") {
    const entries = Object.entries(value);

    for (const [, item] of entries) {
      if (
        typeof item === "number" ||
        typeof item === "string"
      ) {
        return formatValue(item);
      }
    }
  }

  return "Available";
}


export default Dashboard;