# Deployment

The project deploys as two separate services.

| Part | Folder | Host (suggested) |
|---|---|---|
| Backend (FastAPI + model) | repository root | Render web service, free plan |
| Frontend (React + Vite) | `frontend/` | Vercel (free) |

## 1. Add the urban datasets

`/api/urban-data`, `/api/recommendations` and `/api/report` read the files in
`data/external/` (see the report, Table 3.4). Copy them into the repo and commit:

```
data/external/traffic/banglore_traffic.csv
data/external/population/ward_population.csv
data/external/weather/weather.csv
data/external/accidents/accidents.csv
data/external/amenities/{hospitals,schools,bus_stops,metro,parks}.geojson
data/external/mapping/location_mapping.csv
data/external/boundaries/wards.geojson
```

`.gitignore` keeps `data/external/` tracked while the training images stay ignored.
Without these files the API still starts and `/api/analyze` works.

## 2. Backend on Render

Either use the included `render.yaml` (New > Blueprint), or create a Web Service manually:

- Root directory: *(blank — repository root)*
- Build command: `pip install -r requirements-backend.txt`
- Start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
- Instance: Free (512 MB). The API serves `checkpoints/best_model.tflite` with the
  LiteRT runtime instead of full TensorFlow and peaks at about 414 MB.
- Free services sleep after 15 minutes without traffic; the first request after
  that takes about a minute while the service wakes up.
- Environment: `PYTHON_VERSION=3.11.9`, `FRONTEND_ORIGINS=https://<your-frontend>.vercel.app`

Check `https://<your-backend>.onrender.com/health` returns `{"status":"healthy"}`.

## 3. Frontend on Vercel

- Import the repository, Root Directory: `frontend`
- Framework preset: Vite (build `npm run build`, output `dist`)
- Environment variable: `VITE_API_URL=https://<your-backend>.onrender.com`

`frontend/vercel.json` makes page refreshes on `/analysis`, `/dashboard` and
`/recommendations` work. After the first deploy, put the Vercel URL into
`FRONTEND_ORIGINS` on Render.

## Updating the model

After retraining, regenerate the TFLite file so the API serves the new weights:

```
python export_tflite.py
```

If `checkpoints/best_model.tflite` is missing, the API falls back to
`best_model.keras`, which needs TensorFlow and about 810 MB of memory.

## Local development

```
pip install -r requirements-backend.txt   # on Windows use: pip install -r requirements.txt
uvicorn backend.app.main:app --reload          # from the repository root
cd frontend && npm install && npm run dev      # uses http://127.0.0.1:8000 by default
```
