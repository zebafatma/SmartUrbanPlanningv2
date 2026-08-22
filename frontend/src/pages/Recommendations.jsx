import { useEffect, useState } from "react";
import { getRecommendations } from "../services/api";
import "./Recommendations.css";

function Recommendations() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    setLoading(true);
    setError("");

    try {
      const storedAnalysis =
        sessionStorage.getItem("urbanAnalysis");

      if (!storedAnalysis) {
        throw new Error(
          "Please analyze a satellite image before viewing recommendations."
        );
      }

      const analysis = JSON.parse(storedAnalysis);

      const area = analysis.area;
      const ward = analysis.ward;

      const segmentationStatistics =
        analysis.statistics;

      if (!area || !ward) {
        throw new Error(
          "Analysis location is not available. Please select an area and analyze an image first."
        );
      }

      if (!segmentationStatistics) {
        throw new Error(
          "Segmentation results are not available."
        );
      }

      const data = await getRecommendations(
        area,
        ward,
        segmentationStatistics
      );

      setRecommendations(
        normalizeRecommendations(data)
      );
    } catch (err) {
      setError(
        err.message ||
          "Unable to load recommendations."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="recommendations-page">

      {/* ======================================================
          HEADER
          ====================================================== */}

      <section className="recommendations-header">

        <div>

          <span className="recommendations-eyebrow">
            PLANNING INSIGHTS
          </span>

          <h1>
            Turn data into
            <span> better decisions.</span>
          </h1>

          <p>
            Recommendations generated from the
            analyzed urban environment and the
            available city data.
          </p>

        </div>


        <div className="recommendations-status">

          <span />

          <div>
            <small>ANALYSIS STATUS</small>
            <strong>
              {recommendations.length > 0
                ? "Insights available"
                : "Waiting for analysis"}
            </strong>
          </div>

        </div>

      </section>


      {/* ======================================================
          LOADING
          ====================================================== */}

      {loading && (

        <div className="recommendations-loading">

          <span className="recommendations-spinner" />

          <div>
            <strong>
              Generating planning insights
            </strong>

            <p>
              Combining the available urban data...
            </p>
          </div>

        </div>

      )}


      {/* ======================================================
          ERROR
          ====================================================== */}

      {!loading && error && (

        <div className="recommendations-error">

          <div className="recommendation-error-icon">
            !
          </div>

          <div>

            <strong>
              Recommendations unavailable
            </strong>

            <p>
              {error}
            </p>

          </div>

          <button
            type="button"
            onClick={loadRecommendations}
          >
            Retry
          </button>

        </div>

      )}


      {/* ======================================================
          EMPTY
          ====================================================== */}

      {!loading &&
        !error &&
        recommendations.length === 0 && (

          <section className="recommendations-empty">

            <div className="empty-recommendation-icon">
              ✦
            </div>

            <span className="recommendations-eyebrow">
              NO INSIGHTS YET
            </span>

            <h2>
              Analyze an urban area first.
            </h2>

            <p>
              Once your satellite image and urban
              data have been analyzed, planning
              recommendations will appear here.
            </p>

          </section>

        )}


      {/* ======================================================
          RECOMMENDATIONS
          ====================================================== */}

      {!loading &&
        !error &&
        recommendations.length > 0 && (

          <section className="recommendation-results">

            <div className="recommendation-results-heading">

              <div>

                <span className="section-number">
                  01
                </span>

                <div>

                  <h2>
                    Priority actions
                  </h2>

                  <p>
                    Areas that may require attention
                    based on the available data.
                  </p>

                </div>

              </div>

              <span className="recommendation-count">
                {recommendations.length} insights
              </span>

            </div>


            <div className="recommendation-list">

              {recommendations.map(
                (recommendation, index) => (

                  <RecommendationCard
                    key={
                      recommendation.id ||
                      index
                    }
                    recommendation={
                      recommendation
                    }
                    index={index}
                  />

                )
              )}

            </div>

          </section>

        )}

    </main>
  );
}


/* ==========================================================
   Recommendation Card
   ========================================================== */

function RecommendationCard({
  recommendation,
  index,
}) {
  const priority =
    getPriority(recommendation);

  const title =
    recommendation.title ||
    recommendation.name ||
    recommendation.recommendation ||
    "Planning recommendation";

  const description =
    recommendation.description ||
    recommendation.reason ||
    recommendation.explanation ||
    recommendation.message ||
    "";

  const impact =
    recommendation.impact ||
    recommendation.impact_level ||
    "";

  const confidence =
    recommendation.confidence ??
    recommendation.confidence_score ??
    null;

  return (
    <article className="recommendation-card">

      <div className="recommendation-card-number">
        {String(index + 1).padStart(2, "0")}
      </div>


      <div className="recommendation-card-content">

        <div className="recommendation-card-top">

          <span
            className={
              `priority-badge ${getPriorityClass(
                priority
              )}`
            }
          >
            {priority}
          </span>

        </div>


        <h3>
          {title}
        </h3>


        {description && (
          <p>
            {description}
          </p>
        )}


        <div className="recommendation-meta">

          {impact && (
            <div>

              <span>
                IMPACT
              </span>

              <strong>
                {impact}
              </strong>

            </div>
          )}


          {confidence !== null && (
            <div>

              <span>
                CONFIDENCE
              </span>

              <strong>
                {formatConfidence(
                  confidence
                )}
              </strong>

            </div>
          )}

        </div>

      </div>


      <div className="recommendation-arrow">
        →
      </div>

    </article>
  );
}


/* ==========================================================
   Normalize API Response
   ========================================================== */

function normalizeRecommendations(data) {
  if (!data) {
    return [];
  }

  if (Array.isArray(data)) {
    return data;
  }

  if (Array.isArray(data.recommendations)) {
    return data.recommendations;
  }

  if (Array.isArray(data.data)) {
    return data.data;
  }

  if (Array.isArray(data.results)) {
    return data.results;
  }

  return [];
}


/* ==========================================================
   Helpers
   ========================================================== */

function getPriority(recommendation) {
  const value =
    recommendation.priority ||
    recommendation.priority_level ||
    recommendation.severity ||
    "";

  if (!value) {
    return "PRIORITY";
  }

  return String(value).toUpperCase();
}


function getPriorityClass(priority) {
  const value =
    String(priority).toLowerCase();

  if (
    value.includes("high") ||
    value.includes("critical")
  ) {
    return "high";
  }

  if (value.includes("medium")) {
    return "medium";
  }

  if (value.includes("low")) {
    return "low";
  }

  return "default";
}


function formatConfidence(value) {
  const number = Number(value);

  if (Number.isNaN(number)) {
    return value;
  }

  if (number <= 1) {
    return `${Math.round(number * 100)}%`;
  }

  return `${Math.round(number)}%`;
}


export default Recommendations;