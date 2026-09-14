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

## QA

**Verdict: Fail**

### What was tested
- Branch: `feature/003-tasks_by_priority_chart`, worktree `.claude/worktrees/feature-003-tasks_by_priority_chart`.
- Note: this task file was found in `.claude/tasks/doing/` (not yet moved to `quality_assurance/`) at the time of
  testing, but the branch already had a complete implementation commit
  (`363cf15 feat(client): add tasks-by-priority chart page`), so QA proceeded anyway per explicit request.
- Ran `npm test` inside the worktree → 16/16 backend Jest tests passed (unrelated to this frontend-only change).
- Confirmed via `git diff` that no backend files (`api/`, `database/`, models) were touched — only `client/*` and
  `.claude/tasks/doing/feature-003-...md` changed. Backend contract requirement satisfied.
- Started the stack with `./scripts/docker-up.sh` (server on host port 3003). Since the app's `Dockerfile` bakes
  `VITE_API_URL=http://localhost:3001` at build time regardless of the worktree's actual host port (pre-existing
  infra issue, out of scope for this task), set up a temporary local Node TCP proxy from `localhost:3001` →
  `localhost:3003` purely for QA purposes (not part of the codebase) so the built frontend could reach its own
  backend in the browser.
- Ran DB migrations (`docker compose exec server npx sequelize db:migrate`) — already up to date.
- With Playwright, verified in browser at `http://localhost:3001/`:
  - Empty DB state: Home page shows "Nenhuma tarefa por aqui" and a "Ver gráfico por prioridade" link with
    `FaChartBar` icon. Clicking it navigates to `/tasks/by-priority`, which correctly shows its own empty state
    ("Nenhuma tarefa por aqui... Adicione tarefas na tela principal...") instead of a broken/empty chart.
    "← Voltar para Tarefas" link navigates back to `/`.
  - Seeded 3 "importante" tasks and 2 "normal" tasks via `POST /api/tarefas`. Reloaded home page — all 5 tasks
    listed correctly, existing "Marcar/Remover importante" and "Excluir" buttons still present and unchanged.
  - Navigated to `/tasks/by-priority`: a horizontal bar chart (shadcn `ChartContainer` + Recharts `BarChart`)
    renders with two bars, "Importante" and "Normal". Hovering each bar shows a tooltip with the exact count
    (`Importante 3`, `Normal 2`), matching the seeded data.
  - No console errors/warnings; all network requests (`/api/tarefas`, `/api/versao`, `/api/cache-config`)
    returned 200.
  - Cleaned up seeded data via `DELETE /api/tarefas` afterward.
- Tore down the stack with `./scripts/docker-down.sh` and removed the temporary QA-only proxy process.

### Bug found (repro steps)
1. Start the app with at least one "importante" and one non-important task so both bars render.
2. Navigate to `/tasks/by-priority`.
3. Look at the Y-axis category label for the top bar.

**Expected:** the label reads "Importante" in full, clearly readable, consistent with the "Normal" label below it.

**Actual:** the "Importante" label is clipped on its left edge, rendering as "nportante" (missing the "Im"). This
reproduces consistently across viewport widths (tested at both the app's default ~945px window and a resized
1280x900 window) and in both light/dark — it's not a one-off rendering flake. Root cause appears to be the
Recharts `YAxis` category tick label overflowing slightly past the left edge of the app's global `.container`
element, which has `overflow: hidden` (`client/src/index.css`); the chart's `margin={{ left: 12 }}` in
`TasksByPriority.jsx` isn't enough to keep the auto-sized "Importante" label (the longer of the two labels) fully
inside the visible/clipped area, while the shorter "Normal" label happens to fit.

This directly affects the acceptance criterion "The page renders a chart ... with one data point/bar per priority
level, showing the correct count of tasks for each" — the counts are correct (verified via tooltip), but one of
the two category labels is not readable as rendered.

### Suggested fix direction (for dev)
Increase the chart's left margin / YAxis width (or reduce the Card/CardContent left padding, or set a fixed
`width` on `YAxis`) so the longest label ("Importante") renders fully inside the chart/container bounds at the
app's default ~480px-wide layout.

Additionally, while fixing the label clipping, please also make the bars themselves smaller/thinner (both the
bar thickness and overall chart height feel oversized relative to the rest of the app's compact ~480px-wide card
layout) — reduce `barSize`/bar category gap and/or the `ChartContainer` min-height so the chart looks proportional
to the rest of the page instead of dominating it.

## Rework (dev)

Both issues fixed in `client/src/components/TasksByPriority.jsx`:

- **Label clipping:** gave the `YAxis` an explicit `width={88}` (previously relying on Recharts' default
  width of 60px, which wasn't enough to fit "Importante" plus `tickMargin`, so the tick `<text>` was
  rendered partly outside the chart's own `<svg>` bounds and got clipped by it — not actually a `.container`
  overflow issue, the text never fit inside the SVG's own coordinate space to begin with). Also reduced
  `tickMargin` to 8 and tightened the chart's outer `margin` (`left: 4, right: 16, top: 4, bottom: 4`) so the
  reserved axis width is used efficiently.
- **Oversized bars/chart:** removed the `min-h-[220px]` + default `aspect-video` combo (which forced a tall,
  16:9-ish chart) in favor of an explicit `aspect-auto h-[140px]` on `ChartContainer`, and added
  `barSize={18}` + `barCategoryGap="35%"` on `BarChart` so bars are noticeably thinner, proportional to the
  app's compact ~480px-wide card.

Verified with a headless Chrome (Playwright) pass against the rebuilt Docker image, at both the app's default
~500px width and a resized 1280x900 window, in light and dark themes:
- Both "Importante" and "Normal" Y-axis labels render fully, no clipping.
- Chart height/bar thickness now look proportional to the rest of the compact card layout instead of
  dominating it.
- Tooltip on hover still shows the correct per-category count (spot-checked: 1 "Importante" task → tooltip
  shows "Importante 1").
- Empty state (zero tasks) still renders its message correctly, no console errors.
- `npm test` (backend Jest suite) still 16/16 passing, untouched.
