# Frontend — WTP Pension Prototyping Engine (Use Case 1)

React + TypeScript + Chakra UI v3 (Vite), styled with the **CloudNation** brand
system (Marvelblauw, Pastinaak, Epilogue/Mulish). It drives the Use Case 1
comparison: select the fund + benchmark documents, run the analysis, and read the
`FundComparisonReport` — per-area gaps, severity, actuarial impact, proposed Qwik
config, and collapsible source provenance.

## Setup

```bash
cd frontend
npm install
```

## Run

```bash
npm run dev            # http://localhost:5173
```

API calls to `/api/*` are proxied to the FastAPI backend at `http://localhost:8000`
(see `vite.config.ts`) — start the backend too.

## Build

```bash
npm run build          # type-check + production bundle
npm run preview
```

## Structure

```
src/
  theme.ts                       # CloudNation brand system (createSystem)
  api/{client,analysis}.ts       # typed fetch + Use Case 1 endpoints
  pages/ComparisonPage.tsx       # document selection + run + results
  components/
    DocumentSelector.tsx         # fund / benchmark pickers
    EntitlementCard.tsx          # one comparison area (gap, severity, Qwik config, sources)
```
