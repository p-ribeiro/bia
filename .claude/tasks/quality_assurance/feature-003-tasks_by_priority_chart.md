# Feature 003 - Tasks by Priority Chart Page

## User Story

**As a** user of the BIA application
**I want** a new page that shows how many tasks exist grouped by priority, displayed as a graph
**So that** I can quickly understand the distribution of my tasks by priority level at a glance

## Context / Motivation

Today the main "Tasks" page only lists tasks individually, with no aggregated/visual view of how tasks are
distributed across priority levels. Adding a dedicated chart page gives users a quick overview without having to
manually count or filter tasks.

## Requirements

1. Create a **new page** (e.g. `/tasks/by-priority` or similar route consistent with existing client routing
   conventions) that displays the count of tasks grouped by priority.
2. The data must be displayed **as a graph/chart**, built using the **shadcn** component library
   (shadcn's chart components, which wrap Recharts).
   - If `shadcn` is not yet installed/configured in the `client` project, add and configure it following its
     standard setup for a Vite + React project, without disrupting existing UI/styling.
3. The chart should group tasks by their existing `priority` field/values and show a count per priority
   (e.g., a bar chart with one bar per priority level and the number of tasks as the value).
4. Data source:
   - Prefer reusing the existing `/api/tarefas` endpoint (or equivalent existing endpoint that already returns
     tasks with their priority) and aggregate/group the counts on the **frontend**.
   - Do **not** change the backend data contract. Only create a new backend endpoint if grouping purely on the
     frontend is not feasible with existing data (if so, keep the new endpoint additive/non-breaking and clearly
     note it in the PR).
5. Add a **link from the main "Tasks" page** to this new page (e.g., a button or nav link such as "Ver gráfico por
   prioridade" / "View priority chart"), so users can navigate to it easily.
6. The new page should also provide a way to navigate back to the main "Tasks" page.
7. Handle edge cases gracefully:
   - No tasks at all → show an empty state message instead of a broken/empty chart.
   - Priorities with zero tasks → optionally omit or show as zero, consistent with a clean chart presentation.

## Acceptance Criteria

- [x] A new route/page exists in the client app dedicated to showing tasks grouped by priority.
- [x] The page renders a chart (using shadcn chart components) with one data point/bar per priority level,
      showing the correct count of tasks for each.
- [x] The counts shown match the actual number of tasks per priority currently in the system (spot-checked
      against the main Tasks list).
- [x] The main "Tasks" page contains a visible link/button that navigates to the new chart page.
- [x] The new chart page contains a way to navigate back to the main "Tasks" page.
- [x] No changes are made to the existing backend data contract (request/response shapes for existing endpoints
      remain unchanged), unless a new additive endpoint was explicitly required and documented.
- [x] Empty state (zero tasks) is handled without errors or a broken UI.
- [x] Existing Tasks page functionality is unaffected by this change.

## Dev Notes (implementation summary)

- The project's `Tarefas` model only has a boolean `importante` field (no multi-level `priority` field exists
  in the DB). This field is the de-facto "priority" indicator in the app (star icon = "Importante" priority
  vs. "Normal"). The new chart groups tasks into these two levels, derived 100% client-side from the tasks
  already fetched via the existing `/api/tarefas` endpoint. No backend/API changes were made.
- `shadcn` was not previously configured in `client/`. Set it up for this Vite + React (JS) project:
  - Added Tailwind CSS v4 (`tailwindcss` + `@tailwindcss/vite`, as devDependencies) and the `@` path alias
    (`vite.config.js`, `jsconfig.json`).
  - Only imported Tailwind's `theme` and `utilities` layers in `src/index.css` (not `preflight`/base reset),
    specifically to avoid disrupting the app's existing hand-rolled CSS.
  - Added shadcn's CSS variables (`--background`, `--primary`, `--chart-1..5`, etc.) for both light and dark
    themes in `src/index.css`, alongside (not replacing) the app's existing `--bg-*`/`--accent-*` variables.
  - Created `components.json` and ran `npx shadcn@latest add chart button card`, which generated
    `client/src/components/ui/{chart,button,card}.jsx`.
  - Removed a stray, untracked `client/yarn.lock` that wasn't in use (project uses npm per `package.json`
    scripts and `Dockerfile`) — it was making the shadcn CLI try to invoke `yarn`, which isn't installed.
- New page: `client/src/components/TasksByPriority.jsx`, routed at `/tasks/by-priority` in `client/src/App.jsx`.
  Uses shadcn's `Card` + `ChartContainer`/Recharts `BarChart` (horizontal bars, one per priority level).
  Shows an empty-state message when there are no tasks, and a "← Voltar para Tarefas" link back to `/`.
- Added a "Ver gráfico por prioridade" link on the main Tasks page (`HomePage` in `App.jsx`) pointing to the
  new route.
- Verified: `npm run build` succeeds, Docker image builds and serves the new route (HTTP 200), backend Jest
  suite (`npm test`, 16 tests) still passes untouched, and `/api/tarefas` counts were spot-checked against
  seeded tasks (1 "importante" + 2 "normal" matched the chart data).

## Notes for the Dev Agent

- This is primarily a **frontend** feature. Prefer aggregating priority counts client-side from existing task
  data already being fetched, to avoid backend changes.
- Follow the existing project structure/conventions under `client/` for pages, routing, and components.
- Use shadcn's chart component (built on Recharts) for the graph — check shadcn docs for the `chart` component
  setup (`npx shadcn add chart` or equivalent) and follow its recommended pattern (chart config + `ChartContainer`).
- Keep styling consistent with the rest of the app.
- Do not modify backend code, database migrations, or existing API contracts unless strictly necessary and
  clearly called out.

## Priority

Medium — adds a useful reporting/visualization feature without touching core task management functionality.
