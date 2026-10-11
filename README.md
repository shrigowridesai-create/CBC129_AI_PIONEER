# SchedulAI frontend handoff

This package contains the React/Vite frontend source. It excludes `node_modules` and the generated `dist` build so the recipient can install dependencies and build from source.

## Run locally

1. Install Node.js (LTS).
2. From this folder, run `npm ci`.
3. Run `npm run dev` and open the local URL printed by Vite.
4. Run `npm run build` to create a production build in `dist/`.

## Frontend/backend integration

The current app uses demo/local data. `src/services/api.js` contains an optional HTTP adapter with example routes for schedules, meetings, room availability, and room bookings. Confirm endpoint paths and request/response schemas with the backend owner before wiring it into the UI. The adapter accepts a `baseUrl` and uses browser `fetch`.

## Main files

- `src/App.jsx` — application UI and flows
- `src/styles.css` — styling
- `src/data/demo.js` — demo data
- `src/services/api.js` — optional HTTP API adapter
- `src/services/scheduling.js`, `src/utils/time.js` — scheduling and time helpers
