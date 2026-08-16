const API_URL = "http://127.0.0.1:8000";


// ==========================================================
// Analyze Image
// ==========================================================

export async function analyzeImage(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_URL}/api/analyze`,
    {
      method: "POST",
      body: formData,
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Image analysis failed."
    );
  }

  return data;
}


// ==========================================================
// Urban Data
// ==========================================================

export async function getUrbanData(
  area,
  ward
) {
  const params = new URLSearchParams({
    area,
    ward,
  });

  const response = await fetch(
    `${API_URL}/api/urban-data/?${params.toString()}`
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to load urban data."
    );
  }

  return data;
}


// ==========================================================
// Recommendations
// ==========================================================

export async function getRecommendations(
  area,
  ward,
  segmentationStatistics
) {
  const response = await fetch(
    `${API_URL}/api/recommendations/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        area,
        ward,
        segmentation_statistics:
          segmentationStatistics,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
        "Failed to generate recommendations."
    );
  }

  return data;
}


// ==========================================================
// Report
// ==========================================================

export async function generateReport(
  area,
  ward,
  segmentationStatistics,
  weatherDate = null,
  accidentYear = null
) {
  const response = await fetch(
    `${API_URL}/api/report/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        area,
        ward,
        segmentation_statistics:
          segmentationStatistics,
        weather_date: weatherDate,
        accident_year: accidentYear,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
        "Failed to generate report."
    );
  }

  return data;
}