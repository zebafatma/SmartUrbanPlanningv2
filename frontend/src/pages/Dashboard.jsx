import { useEffect, useState } from "react";
import { getUrbanData } from "../services/api";
import "./Dashboard.css";

function Dashboard() {
  const [urbanData, setUrbanData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [location, setLocation] = useState({
    area: "",
    ward: "",
  });


  // ==========================================================
  // Load Urban Data
  // ==========================================================

 useEffect(() => {
  const loadUrbanData = async () => {
    setLoading(true);
    setError("");

    try {
      const storedAnalysis =
        sessionStorage.getItem("urbanAnalysis");

      if (!storedAnalysis) {
        throw new Error(
          "Please select an area and complete an analysis first."
        );
      }

      const analysis = JSON.parse(
        storedAnalysis
      );

      const area = analysis.area;
      const ward = analysis.ward;

      if (!area || !ward) {
        throw new Error(
          "Analysis location is not available."
        );
      }

      setLocation({
        area,
        ward
      });

      const data = await getUrbanData(
        area,
        ward
      );

      setUrbanData(data);
    } catch (err) {
      setError(
        err.message ||
          "Failed to load urban data."
      );
    } finally {
      setLoading(false);
    }
  };

  loadUrbanData();
}, []);


  // ==========================================================
  // Land Cover
  // ==========================================================

  const landCover = getStoredLandCover();


  return (
    <main className="dashboard-page">

      {/* ====================================================
          Header
          ==================================================== */}

      <section className="dashboard-header">

        <div className="dashboard-header-content">

          <span className="section-tag">
            URBAN DASHBOARD
          </span>

          <h1>
            Urban
            <span> Overview</span>
          </h1>

          <p>
            A consolidated view of the selected
            area's environmental and urban
            conditions.
          </p>

        </div>


        <div className="location-card">

          <span className="location-label">
            ANALYSIS AREA
          </span>

          <strong>
            {location.area}
          </strong>

          <small>
            {location.ward}
          </small>

        </div>

      </section>


      {/* ====================================================
          Loading
          ==================================================== */}

      {loading && (

        <div className="dashboard-state">

          <span className="dashboard-spinner" />

          <div>
            <strong>
              Loading urban data
            </strong>

            <span>
              Gathering conditions for {location.area}.
            </span>
          </div>

        </div>

      )}


      {/* ====================================================
          Error
          ==================================================== */}

      {error && (

        <div className="dashboard-error">

          <div className="dashboard-error-icon">
            !
          </div>

          <div>
            <strong>
              Unable to load urban data
            </strong>

            <span>
              {error}
            </span>
          </div>

        </div>

      )}


      {/* ====================================================
          Dashboard Content
          ==================================================== */}

      {!loading && !error && urbanData && (

        <section className="dashboard-content">


          {/* ==================================================
              Key Conditions
              ================================================== */}

          <section className="dashboard-section">

            <div className="dashboard-section-heading">

              <div>

                <span className="section-tag">
                  KEY CONDITIONS
                </span>

                <h2>
                  Urban conditions
                </h2>

              </div>

              <span className="section-description">
                Current data available for the
                selected area.
              </span>

            </div>


            <div className="metric-grid">

              <MetricCard
                label="Traffic"
                value={
                  getPrimaryValue(
                    urbanData.traffic,
                    "Available"
                  )
                }
                icon="↗"
              />

              <MetricCard
                label="Population"
                value={
                  getPrimaryValue(
                    urbanData.population,
                    "Available"
                  )
                }
                icon="◎"
              />

              <MetricCard
                label="Weather"
                value={
                  getPrimaryValue(
                    urbanData.weather,
                    "Available"
                  )
                }
                icon="☼"
              />

              <MetricCard
                label="Accidents"
                value={
                  getPrimaryValue(
                    urbanData.accidents,
                    "Available"
                  )
                }
                icon="!"
              />

            </div>

          </section>


          {/* ==================================================
              Land Cover
              ================================================== */}

          {landCover && (

            <section className="dashboard-section land-cover-section">

              <div className="dashboard-section-heading">

                <div>

                  <span className="section-tag">
                    SATELLITE ANALYSIS
                  </span>

                  <h2>
                    Land-cover distribution
                  </h2>

                </div>

                <span className="section-description">
                  AI classification from the latest
                  satellite analysis.
                </span>

              </div>


              <div className="land-cover-grid">

                {landCover.map(
                  ({
                    name,
                    value,
                    className,
                  }) => (

                    <div
                      className="land-cover-card"
                      key={name}
                    >

                      <div className="land-cover-card-header">

                        <span
                          className={
                            `land-cover-dot ${className}`
                          }
                        />

                        <span>
                          {name}
                        </span>

                      </div>

                      <strong>
                        {formatPercentage(value)}
                      </strong>

                    </div>

                  )
                )}

              </div>

            </section>

          )}


          {/* ==================================================
              Urban Data
              ================================================== */}

          <section className="dashboard-section">

            <div className="dashboard-section-heading">

              <div>

                <span className="section-tag">
                  URBAN DATA
                </span>

                <h2>
                  Area conditions
                </h2>

              </div>

            </div>


            <div className="dashboard-grid">

              <DataCard
                title="Traffic Conditions"
                data={urbanData.traffic}
              />

              <DataCard
                title="Population"
                data={urbanData.population}
              />

              <DataCard
                title="Weather"
                data={urbanData.weather}
              />

              <DataCard
                title="Road Accidents"
                data={urbanData.accidents}
              />

            </div>

          </section>


          {/* ==================================================
              Amenities
              ================================================== */}

          <section className="dashboard-section amenities-section">

            <div className="dashboard-section-heading">

              <div>

                <span className="section-tag">
                  INFRASTRUCTURE
                </span>

                <h2>
                  Urban amenities
                </h2>

              </div>

              <span className="section-description">
                Available facilities and services
                around the selected area.
              </span>

            </div>


            <div className="amenities-grid">

              {Object.entries(
                urbanData.amenities || {}
              )
                .filter(
                  ([name]) =>
                    name !== "Roads" &&
                    name !== "Water"
                )
                .map(
                  ([name, value]) => (

                    <div
                      className="amenity-card"
                      key={name}
                    >

                      <div className="amenity-icon">
                        {getAmenityIcon(name)}
                      </div>

                      <div className="amenity-content">

                        <span>
                          {name}
                        </span>

                        <strong>
                          {getAmenityValue(value)}
                        </strong>

                      </div>

                    </div>

                  )
                )}

            </div>

          </section>


          {/* ==================================================
              Dashboard Footer Insight
              ================================================== */}

          <section className="dashboard-insight">

            <div className="insight-icon">
              ✦
            </div>

            <div>

              <span className="section-tag">
                PLANNING INSIGHT
              </span>

              <h3>
                Use these conditions together
                for better planning decisions.
              </h3>

              <p>
                Combine satellite-derived land
                cover with traffic, population,
                weather, accident and infrastructure
                information to understand the area
                from multiple perspectives.
              </p>

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
}) {
  return (
    <div className="metric-card">

      <div className="metric-icon">
        {icon}
      </div>

      <div className="metric-content">

        <span>
          {label}
        </span>

        <strong>
          {value}
        </strong>

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
}) {
  return (
    <div className="data-card">

      <div className="data-card-header">

        <div>
          <h3>
            {title}
          </h3>
        </div>

        <span className="data-indicator" />

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
            .map(
              ([key, value]) => (

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

              )
            )}

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
      (letter) =>
        letter.toUpperCase()
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


/* ==========================================================
   Primary Value
   ========================================================== */

function getPrimaryValue(
  data,
  fallback = "Available"
) {
  if (!data) {
    return fallback;
  }

  const entries = Object.entries(data);

  /*
   * Prefer common human-readable fields.
   */

  const preferredKeys = [
    "severity",
    "category",
    "classification",
    "population_category",
    "condition",
    "status",
    "temperature",
    "population",
    "population_density",
    "accident_severity_index",
    "infrastructure_score",
  ];

  for (const key of preferredKeys) {

    const entry = entries.find(
      ([entryKey]) =>
        entryKey === key
    );

    if (
      entry &&
      entry[1] !== null &&
      entry[1] !== undefined
    ) {
      return formatValue(entry[1]);
    }
  }


  /*
   * Fallback to the first primitive value.
   */

  for (const [, value] of entries) {

    if (
      value !== null &&
      value !== undefined &&
      typeof value !== "object"
    ) {
      return formatValue(value);
    }

  }

  return fallback;
}


/* ==========================================================
   Amenities
   ========================================================== */

function getAmenityIcon(name) {
  const icons = {
    Hospitals: "✚",
    Schools: "◇",
    "Bus Stops": "●",
    Metro: "◆",
    Parks: "✿",
  };

  return icons[name] || "•";
}


function getAmenityValue(value) {
  if (!value) {
    return "Available";
  }

  if (typeof value === "object") {

    /*
     * AmenityAnalyzer returns objects such as:
     *
     * {
     *   amenity_name,
     *   total_features,
     *   geometry_type,
     *   ...
     * }
     *
     * total_features is the most useful
     * dashboard value.
     */

    if (
      typeof value.total_features === "number"
    ) {
      return `${value.total_features}`;
    }


    const entries =
      Object.entries(value);

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


/* ==========================================================
   Stored Land Cover
   ========================================================== */

function getStoredLandCover() {
  try {

    const stored =
      sessionStorage.getItem(
        "urbanAnalysis"
      );

    if (!stored) {
      return null;
    }

    const parsed =
      JSON.parse(stored);

    const percentages =
      parsed?.statistics?.percentages;

    if (!percentages) {
      return null;
    }

    return [
      {
        name: "Background",
        value:
          percentages.Background ?? 0,
        className: "background",
      },

      {
        name: "Roads",
        value:
          percentages.Road ?? 0,
        className: "road",
      },

      {
        name: "Buildings",
        value:
          percentages.Building ?? 0,
        className: "building",
      },

      {
        name: "Vegetation",
        value:
          percentages.Vegetation ?? 0,
        className: "vegetation",
      },

      {
        name: "Water",
        value:
          percentages.Water ?? 0,
        className: "water",
      },
    ];

  } catch {
    return null;
  }
}


function formatPercentage(value) {
  const number = Number(value);

  if (Number.isNaN(number)) {
    return "0.0%";
  }

  return `${number.toFixed(1)}%`;
}


export default Dashboard;