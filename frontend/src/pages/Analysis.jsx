import { useEffect, useRef, useState } from "react";
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
  // Location Selection
  // ==========================================================

  const [locations, setLocations] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState("");
  const [isLoadingLocations, setIsLoadingLocations] = useState(true);

  useEffect(() => {
    const loadLocations = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/urban-data/locations"
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.detail || "Failed to load Bangalore locations."
          );
        }

        setLocations(data.locations || []);
      } catch (err) {
        setError(
          err.message ||
            "Unable to load Bangalore locations."
        );
      } finally {
        setIsLoadingLocations(false);
      }
    };

    loadLocations();
  }, []);



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
      "image/tiff",
    ];

    const validExtensions = [
      ".png",
      ".jpg",
      ".jpeg",
      ".tif",
      ".tiff",
    ];

    const fileExtension = file.name
      ? `.${file.name.split(".").pop().toLowerCase()}`
      : "";

    const isValidType =
      validTypes.includes(file.type) ||
      validExtensions.includes(fileExtension);

    if (!isValidType) {
      setError(
        "Please upload a PNG, JPG, JPEG or TIFF image."
      );

      return;
    }

    setSelectedFile(file);

    /*
     * TIFF files cannot be reliably displayed directly
     * by the browser.
     *
     * We still create the object URL because it is useful
     * for PNG/JPG/JPEG previews.
     *
     * TIFF files will use the placeholder below.
     */
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
    if (!selectedLocation) {
      setError(
        "Please select a Bangalore area first."
      );

      return;
    }

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

      /*
       * Keep the complete API response in React state.
       *
       * This includes:
       * - statistics
       * - original image
       * - segmentation mask
       * - overlay image
       *
       * React state is fine for these images because they
       * are only needed while this page is open.
       */
      setResult(data);

      /*
       * Keep the latest analysis available for
       * Dashboard / Recommendations later.
       *
       * IMPORTANT:
       * Do NOT store the base64 images in sessionStorage.
       * They are too large and can exceed the browser
       * storage quota.
       */
      sessionStorage.setItem(
        "urbanAnalysis",
        JSON.stringify({
          success: data.success,
          statistics: data.statistics,
          area: selectedLocation,
          ward: selectedLocation,
        })
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


  // ==========================================================
  // Helpers
  // ==========================================================

  const isTiffFile =
    selectedFile &&
    (
      selectedFile.type === "image/tiff" ||
      selectedFile.name
        ?.toLowerCase()
        .endsWith(".tif") ||
      selectedFile.name
        ?.toLowerCase()
        .endsWith(".tiff")
    );


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

      {/* ======================================================
          Location Selection
          ====================================================== */}

      <section className="analysis-location-section">

        <div className="analysis-location-heading">

          <div>
            <span className="location-section-label">
              ANALYSIS LOCATION
            </span>

            <h2>
              Choose an area in Bangalore
            </h2>

            <p>
              Select the area you want to analyze. This location
              will be used for urban data and recommendations.
            </p>
          </div>

        </div>

        <div className="analysis-location-select-wrapper">

          <select
            className="analysis-location-select"
            value={selectedLocation}
            onChange={(event) => {
              setSelectedLocation(event.target.value);
              setError("");
            }}
            disabled={isLoadingLocations || isAnalyzing}
          >

            <option value="">
              {isLoadingLocations
                ? "Loading Bangalore areas..."
                : "Select an area"}
            </option>

            {locations.map((location) => (
              <option
                key={location.ward_no}
                value={location.ward_name}
              >
                {location.ward_name}
                {location.zone
                  ? ` — ${location.zone}`
                  : ""}
              </option>
            ))}

          </select>

        </div>

      </section>


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
              analyze for the selected area.
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
              accept=".png,.jpg,.jpeg,.tif,.tiff,image/png,image/jpeg,image/tiff"
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
              PNG · JPG · JPEG · TIFF
            </span>

          </div>

        ) : (

          <div className="image-preview-container">

            <div className="preview-image-wrapper">

              {isTiffFile && result?.images?.original ? (

                <img
                  src={result.images.original}
                  alt="Analyzed satellite image"
                  className="satellite-preview"
                />
              ) : isTiffFile ? (

                <div className="tiff-preview">

                  <div className="tiff-preview-icon">
                    ◎
                  </div>

                  <strong>
                    TIFF satellite image
                  </strong>

                  <span>
                    Image ready for AI analysis
                  </span>

                </div>

              ) : (

                <img
                  src={preview}
                  alt="Satellite preview"
                  className="satellite-preview"
                />

              )}

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


          {/* ==================================================
              Visual Analysis
              ================================================== */}

          {result.images && (

            <section className="analysis-images-section">

              <div className="analysis-images-heading">

                <div>

                  <span className="workspace-number">
                    03
                  </span>

                  <h3>
                    Visual analysis
                  </h3>

                  <p>
                    Compare the original satellite image
                    with the AI segmentation and analysis
                    overlay.
                  </p>

                </div>

              </div>
              
              {/* Mask legend */}

              <div className="mask-legend">

                <span className="mask-legend-title">
                  Mask legend
                </span>

                <div className="mask-legend-items">

                  <div className="mask-legend-item">
                    <span className="legend-color background" />
                    <span>Background</span>
                  </div>

                  <div className="mask-legend-item">
                    <span className="legend-color road" />
                    <span>Roads</span>
                  </div>

                  <div className="mask-legend-item">
                    <span className="legend-color building" />
                    <span>Buildings</span>
                  </div>

                  <div className="mask-legend-item">
                    <span className="legend-color vegetation" />
                    <span>Vegetation</span>
                  </div>

                  <div className="mask-legend-item">
                    <span className="legend-color water" />
                    <span>Water</span>
                  </div>

                </div>

              </div>

              <div className="analysis-images-grid">

                {/* --------------------------------------------
                    Original
                    -------------------------------------------- */}

                <div className="analysis-image-card">

                  <div className="analysis-image-header">

                    <div>
                      <h3>
                        Original image
                      </h3>

                      <span>
                        Satellite
                      </span>
                    </div>

                  </div>


                  <div className="analysis-image-wrapper">

                    <img
                      src={result.images.original}
                      alt="Original satellite image"
                    />

                  </div>

                </div>


                {/* --------------------------------------------
                    Segmentation Mask
                    -------------------------------------------- */}

                <div className="analysis-image-card">

                  <div className="analysis-image-header">

                    <div>
                      <h3>
                        Segmentation mask
                      </h3>

                      <span>
                        AI classification
                      </span>
                    </div>

                  </div>


                  <div className="analysis-image-wrapper">

                    <img
                      src={result.images.mask}
                      alt="AI segmentation mask"
                    />

                  </div>

                </div>


                {/* --------------------------------------------
                    Overlay
                    -------------------------------------------- */}

                <div className="analysis-image-card">

                  <div className="analysis-image-header">

                    <div>
                      <h3>
                        Analysis overlay
                      </h3>

                      <span>
                        Combined view
                      </span>
                    </div>

                  </div>


                  <div className="analysis-image-wrapper">

                    <img
                      src={result.images.overlay}
                      alt="Satellite analysis overlay"
                    />

                  </div>

                </div>

              </div>

            </section>

          )}

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
        className={`land-cover-symbol ${className}`}
        aria-hidden="true"
      />

      <div className="land-cover-content">

        <span className="land-cover-name">
          {name}
        </span>

        <strong className="land-cover-value">
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