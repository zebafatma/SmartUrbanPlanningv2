import { Link } from "react-router-dom";
import "./Home.css";

function Home() {
  return (
    <main className="home-page">

      {/* ==========================================================
          HERO
          ========================================================== */}

      <section className="home-hero">

        <div className="home-hero-content">

          <div className="home-eyebrow">
            <span className="eyebrow-dot" />
            AI-POWERED URBAN INTELLIGENCE
          </div>

          <h1>
            Build better cities
            <span> with smarter data.</span>
          </h1>

          <p className="hero-description">
            Analyze satellite imagery and combine it with
            traffic, population, weather, accidents, and
            infrastructure data to understand urban
            environments and make better planning decisions.
          </p>


          <div className="home-actions">

            <Link
              to="/analysis"
              className="home-primary-button"
            >
              Start Analysis
              <span>→</span>
            </Link>

            <a
              href="#how-it-works"
              className="home-secondary-button"
            >
              Explore the Platform
            </a>

          </div>


          {/* Small stats */}

          <div className="home-stats">

            <div className="home-stat">
              <strong>AI</strong>
              <span>Image Analysis</span>
            </div>

            <div className="home-stat-divider" />

            <div className="home-stat">
              <strong>7+</strong>
              <span>Data Sources</span>
            </div>

            <div className="home-stat-divider" />

            <div className="home-stat">
              <strong>5</strong>
              <span>Land Classes</span>
            </div>

          </div>

        </div>


        {/* ======================================================
            VISUAL
            ====================================================== */}

        <div className="home-hero-visual">

          <div className="environment-card">

            <div className="environment-header">

              <div>
                <span>
                  URBAN ENVIRONMENT
                </span>

                <h3>
                  City Analysis
                </h3>
              </div>

              <div className="live-indicator">
                <span />
                Ready
              </div>

            </div>


            {/* Abstract city visualization */}

            <div className="city-map">

              <div className="map-grid" />

              <div className="map-road map-road-1" />
              <div className="map-road map-road-2" />
              <div className="map-road map-road-3" />

              <div className="map-building map-building-1" />
              <div className="map-building map-building-2" />
              <div className="map-building map-building-3" />
              <div className="map-building map-building-4" />
              <div className="map-building map-building-5" />

              <div className="map-green map-green-1" />
              <div className="map-green map-green-2" />

              <div className="map-water" />

              <div className="map-label vegetation-label">
                <span />
                Vegetation
              </div>

              <div className="map-label building-label">
                <span />
                Buildings
              </div>

              <div className="map-label road-label">
                <span />
                Roads
              </div>

            </div>


            {/* Bottom information */}

            <div className="environment-footer">

              <div>
                <span>Coverage</span>
                <strong>92.4%</strong>
              </div>

              <div>
                <span>Land Classes</span>
                <strong>5</strong>
              </div>

              <div>
                <span>Status</span>
                <strong className="status-ready">
                  Ready
                </strong>
              </div>

            </div>

          </div>

        </div>

      </section>


      {/* ==========================================================
          HOW IT WORKS
          ========================================================== */}

      <section
        className="how-section"
        id="how-it-works"
      >

        <div className="home-section-heading">

          <span className="section-label">
            HOW IT WORKS
          </span>

          <h2>
            From raw data to
            <span> urban insight.</span>
          </h2>

          <p>
            A simple workflow that combines AI-powered
            image analysis with real-world urban data.
          </p>

        </div>


        <div className="workflow-grid">

          {/* Step 01 */}

          <div className="workflow-card">

            <div className="workflow-top">

              <span className="workflow-number">
                01
              </span>

              <div className="workflow-icon">
                ◈
              </div>

            </div>

            <h3>
              Analyze satellite imagery
            </h3>

            <p>
              Upload a satellite image and let the
              segmentation model identify roads,
              buildings, vegetation, and water.
            </p>

          </div>


          {/* Step 02 */}

          <div className="workflow-card">

            <div className="workflow-top">

              <span className="workflow-number">
                02
              </span>

              <div className="workflow-icon">
                ◎
              </div>

            </div>

            <h3>
              Understand urban conditions
            </h3>

            <p>
              Combine the image analysis with traffic,
              population, weather, accident, and
              infrastructure information.
            </p>

          </div>


          {/* Step 03 */}

          <div className="workflow-card">

            <div className="workflow-top">

              <span className="workflow-number">
                03
              </span>

              <div className="workflow-icon">
                ✦
              </div>

            </div>

            <h3>
              Get planning recommendations
            </h3>

            <p>
              Turn the combined information into
              practical recommendations for smarter
              and more sustainable development.
            </p>

          </div>

        </div>

      </section>


      {/* ==========================================================
          DATA SOURCES
          ========================================================== */}

      <section className="data-section">

        <div className="data-section-inner">

          <div className="data-section-copy">

            <span className="section-label">
              ONE PLATFORM
            </span>

            <h2>
              Multiple perspectives.
              <span> One urban picture.</span>
            </h2>

            <p>
              Smart Urban Planning brings different
              sources together so that decisions aren't
              based on a single metric.
            </p>

          </div>


          <div className="data-source-list">

            <div className="data-source">
              <span className="source-icon">◈</span>
              <div>
                <strong>Satellite Imagery</strong>
                <span>AI land-cover segmentation</span>
              </div>
            </div>

            <div className="data-source">
              <span className="source-icon">↗</span>
              <div>
                <strong>Traffic</strong>
                <span>Traffic and congestion conditions</span>
              </div>
            </div>

            <div className="data-source">
              <span className="source-icon">◎</span>
              <div>
                <strong>Population</strong>
                <span>Population and infrastructure</span>
              </div>
            </div>

            <div className="data-source">
              <span className="source-icon">✦</span>
              <div>
                <strong>Urban Amenities</strong>
                <span>Schools, hospitals, transport and parks</span>
              </div>
            </div>

          </div>

        </div>

      </section>


      {/* ==========================================================
          CTA
          ========================================================== */}

      <section className="home-cta">

        <div className="cta-content">

          <span className="section-label">
            READY TO EXPLORE?
          </span>

          <h2>
            Start understanding your city.
          </h2>

          <p>
            Upload a satellite image and turn urban
            data into meaningful insight.
          </p>

        </div>


        <Link
          to="/analysis"
          className="cta-button"
        >
          Start Analysis
          <span>→</span>
        </Link>

      </section>

    </main>
  );
}

export default Home;