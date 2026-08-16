import { useRef, useState } from "react";
import { analyzeImage } from "../services/api";
import "./Analysis.css";

function Analysis() {
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);

  const [result, setResult] = useState(null);

  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const [error, setError] = useState("");

  const [isDragging, setIsDragging] = useState(false);


  // ==========================================================
  // File Selection
  // ==========================================================

  const handleFile = (file) => {
    if (!file) {
      return;
    }

    const validTypes = [
      "image/png",
      "image/jpeg",
      "image/jpg",
    ];

    if (!validTypes.includes(file.type)) {
      setError(
        "Please upload a PNG, JPG, or JPEG image."
      );
      return;
    }

    setSelectedFile(file);

    setPreview(
      URL.createObjectURL(file)
    );

    setResult(null);

    setError("");
  };


  const handleFileChange = (event) => {
    handleFile(event.target.files[0]);
  };


  // ==========================================================
  // Drag & Drop
  // ==========================================================

  const handleDragOver = (event) => {
    event.preventDefault();

    setIsDragging(true);
  };


  const handleDragLeave = () => {
    setIsDragging(false);
  };


  const handleDrop = (event) => {
    event.preventDefault();

    setIsDragging(false);

    const file = event.dataTransfer.files[0];

    handleFile(file);
  };


  // ==========================================================
  // Analyze
  // ==========================================================

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError(
        "Please upload a satellite image first."
      );

      return;
    }

    setIsAnalyzing(true);

    setError("");

    setResult(null);

    try {
      const data = await analyzeImage(
        selectedFile
      );

      setResult(data);

      /*
       * Keep the latest analysis available for
       * Dashboard / Recommendations later.
       */

      sessionStorage.setItem(
        "urbanAnalysis",
        JSON.stringify(data)
      );

    } catch (err) {
      setError(
        err.message ||
          "Unable to analyze the image."
      );
    } finally {
      setIsAnalyzing(false);
    }
  };


  // ==========================================================
  // Remove Image
  // ==========================================================

  const handleRemove = () => {
    if (preview) {
      URL.revokeObjectURL(preview);
    }

    setSelectedFile(null);

    setPreview(null);

    setResult(null);

    setError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };


  return (
    <main className="analysis-page">

      {/* ======================================================
          Header
          ====================================================== */}

      <section className="analysis-header">

        <div className="analysis-header-content">

          <span className="analysis-eyebrow">
            URBAN ANALYSIS
          </span>

          <h1>
            Understand your
            <span> urban environment.</span>
          </h1>

          <p>
            Upload a satellite image and let the AI
            segmentation model identify the major
            land-cover features in the selected area.
          </p>

        </div>


        <div className="analysis-model-status">

          <span className="model-status-dot" />

          <div>
            <span>AI MODEL</span>
            <strong>Ready for analysis</strong>
          </div>

        </div>

      </section>


      {/* ======================================================
          Main Workspace
          ====================================================== */}

      <section className="analysis-workspace">

        <div className="analysis-workspace-heading">

          <div>

            <span className="workspace-number">
              01
            </span>

            <h2>
              Satellite imagery
            </h2>

            <p>
              Select the satellite image you want to
              analyze.
            </p>

          </div>

          {selectedFile && (
            <button
              type="button"
              className="remove-image-button"
              onClick={handleRemove}
              disabled={isAnalyzing}
            >
              Remove image
            </button>
          )}

        </div>


        {/* ==================================================
            Upload Area
            ================================================== */}

        {!preview ? (

          <div
            className={
              isDragging
                ? "upload-zone dragging"
                : "upload-zone"
            }
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() =>
              fileInputRef.current?.click()
            }
          >

            <input
              ref={fileInputRef}
              type="file"
              accept=".png,.jpg,.jpeg,image/png,image/jpeg"
              onChange={handleFileChange}
              hidden
            />

            <div className="upload-icon">
              ↑
            </div>

            <h3>
              Drop your satellite image here
            </h3>

            <p>
              or click to select an image from
              your computer
            </p>

            <span className="upload-formats">
              PNG · JPG · JPEG
            </span>

          </div>

        ) : (

          <div className="image-preview-container">

            <div className="preview-image-wrapper">

              <img
                src={preview}
                alt="Satellite preview"
                className="satellite-preview"
              />

              <div className="preview-badge">
                <span />
                Image ready
              </div>

            </div>


            <div className="preview-information">

              <div>

                <span>FILE</span>

                <strong>
                  {selectedFile.name}
                </strong>

              </div>


              <div>

                <span>SIZE</span>

                <strong>
                  {formatFileSize(
                    selectedFile.size
                  )}
                </strong>

              </div>


              <div>

                <span>STATUS</span>

                <strong className="ready-text">
                  Ready
                </strong>

              </div>

            </div>

          </div>

        )}


        {/* ==================================================
            Error
            ================================================== */}

        {error && (
          <div className="analysis-error">
            <span>!</span>
            {error}
          </div>
        )}


        {/* ==================================================
            Analyze Button
            ================================================== */}

        <div className="analysis-action-row">

          <div className="analysis-hint">

            <span>✦</span>

            <p>
              The model will classify pixels into
              background, roads, buildings,
              vegetation and water.
            </p>

          </div>


          <button
            type="button"
            className="analyze-button"
            onClick={handleAnalyze}
            disabled={
              !selectedFile ||
              isAnalyzing
            }
          >

            {isAnalyzing ? (
              <>
                <span className="analysis-spinner" />
                Analyzing...
              </>
            ) : (
              <>
                Analyze Image
                <span>→</span>
              </>
            )}

          </button>

        </div>

      </section>


      {/* ======================================================
          Loading
          ====================================================== */}

      {isAnalyzing && (

        <section className="analysis-progress">

          <div className="progress-content">

            <div className="progress-icon">
              ✦
            </div>

            <div>

              <span>
                AI ANALYSIS IN PROGRESS
              </span>

              <h3>
                Understanding the urban landscape...
              </h3>

              <p>
                Segmenting roads, buildings,
                vegetation, water and background.
              </p>

            </div>

          </div>


          <div className="progress-line">
            <div />
          </div>

        </section>

      )}


      {/* ======================================================
          Results
          ====================================================== */}

      {result && !isAnalyzing && (

        <section className="analysis-results">

          <div className="results-heading">

            <div>

              <span className="analysis-eyebrow">
                ANALYSIS COMPLETE
              </span>

              <h2>
                Land-cover analysis
              </h2>

              <p>
                Distribution detected from the
                uploaded satellite image.
              </p>

            </div>


            <div className="complete-badge">
              <span>✓</span>
              Analysis complete
            </div>

          </div>


          {/* ==================================================
              Statistics
              ================================================== */}

          <div className="land-cover-grid">

            {getPercentages(result).map(
              ({
                name,
                value,
                className,
              }) => (

                <LandCoverCard
                  key={name}
                  name={name}
                  value={value}
                  className={className}
                />

              )
            )}

          </div>


          {/* ==================================================
              Raw Result Information
              ================================================== */}

          <div className="result-summary">

            <div className="result-summary-heading">

              <span className="workspace-number">
                02
              </span>

              <div>
                <h3>
                  Analysis summary
                </h3>

                <p>
                  AI-generated land-cover
                  distribution.
                </p>
              </div>

            </div>


            <div className="coverage-bars">

              {getPercentages(result).map(
                ({
                  name,
                  value,
                  className,
                }) => (

                  <CoverageBar
                    key={name}
                    name={name}
                    value={value}
                    className={className}
                  />

                )
              )}

            </div>

          </div>

        </section>

      )}

    </main>
  );
}


/* ==========================================================
   Land Cover Card
   ========================================================== */

function LandCoverCard({
  name,
  value,
  className,
}) {
  return (
    <div className="land-cover-card">

      <div
        className={
          `land-cover-symbol ${className}`
        }
      />

      <div>

        <span>
          {name}
        </span>

        <strong>
          {formatPercentage(value)}
        </strong>

      </div>

    </div>
  );
}


/* ==========================================================
   Coverage Bar
   ========================================================== */

function CoverageBar({
  name,
  value,
  className,
}) {
  const numericValue =
    Number(value) || 0;

  return (
    <div className="coverage-row">

      <div className="coverage-label">

        <span>
          {name}
        </span>

        <strong>
          {formatPercentage(
            numericValue
          )}
        </strong>

      </div>


      <div className="coverage-track">

        <div
          className={
            `coverage-fill ${className}`
          }
          style={{
            width: `${Math.min(
              Math.max(
                numericValue,
                0
              ),
              100
            )}%`,
          }}
        />

      </div>

    </div>
  );
}


/* ==========================================================
   Helpers
   ========================================================== */

function getPercentages(result) {
  const percentages =
    result?.statistics?.percentages ||
    result?.percentages ||
    result?.segmentation_statistics
      ?.percentages ||
    {};

  return [
    {
      name: "Background",
      value:
        percentages.Background ??
        percentages.background ??
        0,
      className: "background",
    },

    {
      name: "Roads",
      value:
        percentages.Road ??
        percentages.Roads ??
        percentages.road ??
        percentages.roads ??
        0,
      className: "road",
    },

    {
      name: "Buildings",
      value:
        percentages.Building ??
        percentages.Buildings ??
        percentages.building ??
        percentages.buildings ??
        0,
      className: "building",
    },

    {
      name: "Vegetation",
      value:
        percentages.Vegetation ??
        percentages.vegetation ??
        0,
      className: "vegetation",
    },

    {
      name: "Water",
      value:
        percentages.Water ??
        percentages.water ??
        0,
      className: "water",
    },
  ];
}


function formatPercentage(value) {
  const number = Number(value);

  if (Number.isNaN(number)) {
    return "0.0%";
  }

  return `${number.toFixed(1)}%`;
}


function formatFileSize(bytes) {
  if (!bytes) {
    return "0 KB";
  }

  const mb =
    bytes / (1024 * 1024);

  if (mb >= 1) {
    return `${mb.toFixed(2)} MB`;
  }

  return `${(
    bytes / 1024
  ).toFixed(1)} KB`;
}


export default Analysis;