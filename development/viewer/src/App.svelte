<script lang="ts">
  import { onMount, tick } from "svelte";
  import { invoke } from "@tauri-apps/api/core";
  import { open } from "@tauri-apps/plugin-dialog";
  import { Button } from "$lib/components/ui/button";
  import { Badge } from "$lib/components/ui/badge";
  import * as Tabs from "$lib/components/ui/tabs";
  import * as Select from "$lib/components/ui/select";
  import * as Collapsible from "$lib/components/ui/collapsible";
  import PlusIcon from "@lucide/svelte/icons/plus";
  import RefreshCwIcon from "@lucide/svelte/icons/refresh-cw";
  import Trash2Icon from "@lucide/svelte/icons/trash-2";
  import ChevronDownIcon from "@lucide/svelte/icons/chevron-down";
  import PauseIcon from "@lucide/svelte/icons/pause";
  import XIcon from "@lucide/svelte/icons/x";
  import CircleIcon from "@lucide/svelte/icons/circle";
  import PlayIcon from "@lucide/svelte/icons/play";
  import Pagination from "$lib/components/Pagination.svelte";
  import { demoSnapshot, paginationDemoSnapshot } from "./lib/demo";
  import type { Decision, ProjectRegistry, ProjectSnapshot, SavedProject, WorkItem, WorkStatus } from "./lib/types";
  const demoEnabled = import.meta.env.DEV || import.meta.env.VITE_DEMO === "true";
  const demoMode = demoEnabled ? new URLSearchParams(window.location.search).get("demo") : null;
  const isDemo = demoMode !== null;
  const activeDemoSnapshot = demoMode === "pagination" ? paginationDemoSnapshot : demoSnapshot;
  const PAGE_SIZE = 100;

  let projects: SavedProject[] = [];
  let selectedId = "";
  let snapshot: ProjectSnapshot | null = null;
  let selectedPlanId = "";
  let workFilter: "all" | WorkStatus | "blocked" = "all";
  let decisionFilter: "current" | "proposed" | "history" | "all" = "current";
  let workPage = 1;
  let decisionPage = 1;
  let compactPane: "plan" | "decisions" = "plan";
  let loading = false;
  let message = "";
  let error = "";
  let pollTimer: number | undefined;
  let scanRequest = 0;
  let refreshInFlight = false;
  let openWorkItems = new Set<string>();
  let openDecisions = new Set<string>();
  let overviewEntries: Array<{ project: SavedProject; snapshot: ProjectSnapshot | null; error: string }> = [];

  $: selectedProject = projects.find((project) => project.id === selectedId) ?? null;
  $: activePlan = snapshot?.plans.find((plan) => plan.id === snapshot?.active_plan) ?? null;
  $: selectedPlan = snapshot?.plans.find((plan) => plan.id === selectedPlanId) ?? activePlan ?? snapshot?.plans[0] ?? null;
  $: currentItem = selectedPlan?.status === "active"
    ? selectedPlan.work_items.find((item) => item.id === selectedPlan.current_item) ?? null
    : null;
  $: activeCurrentItem = activePlan?.work_items.find((item) => item.id === activePlan.current_item) ?? null;
  $: visibleItems = selectedPlan?.work_items.filter((item) => matchesWorkFilter(item, workFilter)) ?? [];
  $: workPageCount = Math.max(1, Math.ceil(visibleItems.length / PAGE_SIZE));
  $: if (workPage > workPageCount) workPage = workPageCount;
  $: pagedItems = visibleItems.slice((workPage - 1) * PAGE_SIZE, workPage * PAGE_SIZE);
  $: progress = summarizeWork(selectedPlan?.work_items ?? []);
  $: visibleDecisions = snapshot?.decisions.filter((decision) => matchesDecisionFilter(decision, decisionFilter)) ?? [];
  $: decisionPageCount = Math.max(1, Math.ceil(visibleDecisions.length / PAGE_SIZE));
  $: if (decisionPage > decisionPageCount) decisionPage = decisionPageCount;
  $: pagedDecisions = visibleDecisions.slice((decisionPage - 1) * PAGE_SIZE, decisionPage * PAGE_SIZE);
  $: linkedDecisionIds = new Set(activeCurrentItem?.decisions ?? []);

  onMount(() => {
    if (isDemo) {
      projects = [{ id: "demo", name: activeDemoSnapshot.name, path: activeDemoSnapshot.root }];
      selectedId = "demo";
      snapshot = activeDemoSnapshot;
      overviewEntries = [{ project: projects[0], snapshot: activeDemoSnapshot, error: "" }];
      selectedPlanId = activeDemoSnapshot.active_plan ?? activeDemoSnapshot.plans[0]?.id ?? "";
      return;
    }

    void initialize();
    pollTimer = window.setInterval(() => {
      if (!document.hidden && selectedId) refreshVisibleProject();
    }, 4000);

    const handleVisibility = () => {
      if (!document.hidden && selectedId) refreshVisibleProject();
    };
    document.addEventListener("visibilitychange", handleVisibility);
    return () => {
      window.clearInterval(pollTimer);
      document.removeEventListener("visibilitychange", handleVisibility);
    };
  });

  async function initialize() {
    loading = true;
    try {
      const registry = await invoke<ProjectRegistry>("load_project_registry");
      projects = registry.projects;
      selectedId = registry.selected || (projects.length ? "__overview__" : "");
      if (selectedId === "__overview__") await refreshOverview();
      else if (selectedId) {
        await refreshProject(false, projects.find((project) => project.id === selectedId) ?? null);
      }
    } catch (cause) {
      error = readableError(cause);
    } finally {
      loading = false;
    }
  }

  async function saveRegistry(next: SavedProject[], selected: string) {
    await invoke("save_project_registry", {
      registry: { version: 1, selected, projects: next } satisfies ProjectRegistry,
    });
    projects = next;
  }

  async function addProject(replace = false) {
    scanRequest += 1;
    refreshInFlight = false;
    loading = false;
    error = "";
    const path = await open({ directory: true, multiple: false, title: "Choose a Scoville Plan project" });
    if (!path || Array.isArray(path)) return;

    loading = true;
    message = "Reading project…";
    try {
      const loaded = await invoke<ProjectSnapshot>("scan_project", { root: path });
      const existing = projects.find((project) => project.path === loaded.root);
      const entry: SavedProject = existing ?? {
        id: crypto.randomUUID(),
        name: loaded.name,
        path: loaded.root,
      };
      const next = replace && selectedProject
        ? projects.map((project) => (project.id === selectedProject?.id ? { ...entry, id: project.id } : project))
        : existing
          ? projects
          : [...projects, entry];
      const nextSelected = replace && selectedProject ? selectedProject.id : entry.id;
      await saveRegistry(next, nextSelected);
      selectedId = nextSelected;
      snapshot = loaded;
      selectedPlanId = loaded.active_plan ?? loaded.plans[0]?.id ?? "";
      workPage = 1;
      decisionPage = 1;
      message = `${loaded.name} added`;
    } catch (cause) {
      error = readableError(cause);
      message = "";
    } finally {
      loading = false;
    }
  }

  async function selectProject(id: string) {
    scanRequest += 1;
    refreshInFlight = false;
    loading = false;
    if (!isDemo) {
      try {
        await saveRegistry(projects, id);
      } catch (cause) {
        error = readableError(cause);
        return;
      }
    }
    const project = projects.find((entry) => entry.id === id) ?? null;
    selectedId = id;
    snapshot = null;
    selectedPlanId = "";
    workPage = 1;
    decisionPage = 1;
    error = "";
    if (isDemo) {
      if (id === "demo") {
        snapshot = activeDemoSnapshot;
        selectedPlanId = activeDemoSnapshot.active_plan ?? activeDemoSnapshot.plans[0]?.id ?? "";
      }
      return;
    }
    if (id === "__overview__") await refreshOverview();
    else await refreshProject(false, project);
  }

  async function removeProject(id = selectedProject?.id) {
    if (!id || isDemo) return;
    scanRequest += 1;
    refreshInFlight = false;
    loading = false;
    const removed = projects.find((project) => project.id === id);
    const next = projects.filter((project) => project.id !== id);
    const nextSelected = next.length ? "__overview__" : "";
    try {
      await saveRegistry(next, nextSelected);
    } catch (cause) {
      error = readableError(cause);
      return;
    }
    overviewEntries = overviewEntries.filter((entry) => entry.project.id !== id);
    selectedId = nextSelected;
    snapshot = null;
    error = "";
    message = `${removed?.name ?? "Project"} removed from the viewer`;
    if (selectedId) {
      void refreshOverview();
    }
  }

  async function refreshOverview(quiet = false) {
    if (!projects.length || isDemo || (quiet && refreshInFlight)) return;
    const request = ++scanRequest;
    refreshInFlight = true;
    if (!quiet) {
      loading = true;
      message = "Reading projects…";
    }
    try {
      const entries = await Promise.all(projects.map(async (project) => {
        try {
          return { project, snapshot: await invoke<ProjectSnapshot>("scan_project", { root: project.path }), error: "" };
        } catch (cause) {
          return { project, snapshot: null, error: readableError(cause) };
        }
      }));
      if (request === scanRequest && selectedId === "__overview__") overviewEntries = entries;
    } finally {
      if (request === scanRequest) {
        refreshInFlight = false;
        if (!quiet) {
          loading = false;
          message = "";
        }
      }
    }
  }

  function refreshVisibleProject() {
    if (loading || refreshInFlight) return;
    if (selectedId === "__overview__") void refreshOverview(true);
    else void refreshProject(true);
  }

  async function relocateProject(id: string) {
    selectedId = id;
    await addProject(true);
    if (selectedId === id) await selectProject("__overview__");
  }

  async function refreshProject(quiet: boolean, project = selectedProject) {
    if (!project || isDemo || (quiet && (loading || refreshInFlight))) return;
    const request = ++scanRequest;
    refreshInFlight = true;
    if (!quiet) {
      loading = true;
      message = "Reading project…";
    }
    try {
      const loaded = await invoke<ProjectSnapshot>("scan_project", { root: project.path });
      if (request !== scanRequest || selectedId !== project.id) return;
      snapshot = loaded;
      if (!selectedPlanId || !loaded.plans.some((plan) => plan.id === selectedPlanId)) {
        selectedPlanId = loaded.active_plan ?? loaded.plans[0]?.id ?? "";
      }
      error = "";
      message = quiet ? "" : "Project refreshed";
    } catch (cause) {
      if (request !== scanRequest || selectedId !== project.id) return;
      error = readableError(cause);
      message = "";
    } finally {
      if (request === scanRequest) {
        refreshInFlight = false;
        loading = false;
      }
    }
  }

  function readableError(cause: unknown) {
    return typeof cause === "string" ? cause : cause instanceof Error ? cause.message : "The project could not be read.";
  }

  function summarizeWork(items: WorkItem[]) {
    return items.reduce(
      (counts, item) => {
        counts[item.status] += 1;
        return counts;
      },
      { todo: 0, in_progress: 0, paused: 0, done: 0, cancelled: 0 },
    );
  }

  function matchesWorkFilter(item: WorkItem, filter: typeof workFilter) {
    if (filter === "all") return true;
    if (filter === "blocked") return item.blocked_by.length > 0;
    return item.status === filter;
  }

  function matchesDecisionFilter(decision: Decision, filter: typeof decisionFilter) {
    if (filter === "all") return true;
    if (filter === "current") return decision.status === "accepted";
    if (filter === "proposed") return decision.status === "proposed";
    return ["superseded", "deprecated", "rejected"].includes(decision.status);
  }

  function selectPlan(id: string) {
    selectedPlanId = id;
    workPage = 1;
    decisionPage = 1;
  }

  function selectWorkFilter(filter: typeof workFilter) {
    workFilter = filter;
    workPage = 1;
  }

  function selectDecisionFilter(filter: typeof decisionFilter) {
    decisionFilter = filter;
    decisionPage = 1;
  }

  async function selectPage(kind: "work" | "decision", page: number) {
    if (kind === "work") workPage = page;
    else decisionPage = page;
    await tick();
    const pane = document.getElementById(kind === "work" ? "plan-panel" : "decisions-panel");
    const topbarHeight = document.querySelector<HTMLElement>(".topbar")?.offsetHeight ?? 0;
    if (pane) window.scrollTo({ top: pane.getBoundingClientRect().top + window.scrollY - topbarHeight - 16 });
    pane?.querySelector<HTMLElement>(kind === "work" ? ".work-summary" : ".decision-summary")?.focus({ preventScroll: true });
  }

  function workStatusLabel(status: WorkStatus) {
    return ({ todo: "Upcoming", in_progress: "In progress", paused: "Paused", done: "Completed", cancelled: "Cancelled" })[status];
  }

  function stepNumber(index: number, total: number) {
    return String(index + 1).padStart(Math.max(2, String(total).length), "0");
  }

  function decisionStatusLabel(status: Decision["status"]) {
    return ({ proposed: "Proposed", accepted: "Current", rejected: "Rejected", deprecated: "Deprecated", superseded: "Superseded" })[status];
  }

  function decisionById(id: string) {
    return snapshot?.decisions.find((decision) => decision.id === id);
  }

  function setWorkItemOpen(id: string, open: boolean) {
    const next = new Set(openWorkItems);
    open ? next.add(id) : next.delete(id);
    openWorkItems = next;
  }

  function setDecisionOpen(id: string, open: boolean) {
    const next = new Set(openDecisions);
    open ? next.add(id) : next.delete(id);
    openDecisions = next;
  }
</script>

<svelte:head><title>{snapshot ? `${snapshot.name} · ` : ""}Scoville Plan Viewer</title></svelte:head>

<div class="app-shell">
  <header class="topbar" class:without-plan={!snapshot?.plans.length}>
    <a class="brand" href="/" aria-label="Scoville Plan home" onclick={(event) => event.preventDefault()}>
      <span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span>
      <span><strong>Scoville Plan</strong><small>Plan status viewer</small></span>
    </a>

    <div class="project-switcher">
      <span class="control-label" id="project-select-label">Project</span>
      <Select.Root type="single" value={selectedId} onValueChange={(value) => value && void selectProject(value)} disabled={!projects.length || loading}>
        <Select.Trigger class="project-select" aria-labelledby="project-select-label"><span class="select-label">{selectedId === "__overview__" ? "All projects" : selectedProject?.name ?? "No projects added"}</span></Select.Trigger>
        <Select.Content>
          {#if projects.length}<Select.Item value="__overview__" label="All projects" />{/if}
          {#each projects as project}<Select.Item value={project.id} label={project.name} />{/each}
        </Select.Content>
      </Select.Root>
    </div>

    {#if snapshot?.plans.length}
      <div class="plan-selector">
        <label for="plan-select">Plan history</label>
        <Select.Root type="single" value={selectedPlanId} onValueChange={(value) => value && selectPlan(value)}>
          <Select.Trigger id="plan-select" class="plan-select"><span class="select-label">{selectedPlan ? `${selectedPlan.id} · ${selectedPlan.title}` : "Choose plan"}</span></Select.Trigger>
          <Select.Content>{#each snapshot.plans as plan}<Select.Item value={plan.id} label={`${plan.id} · ${plan.title} · ${plan.status}`} />{/each}</Select.Content>
        </Select.Root>
      </div>
    {/if}

    <div class="top-actions">
      <Button aria-label="Add project" onclick={() => void addProject()} disabled={loading || isDemo}><PlusIcon /> <span class="button-label">Add project</span></Button>
      <Button variant="outline" size="icon" title="Refresh project" aria-label="Refresh project" onclick={() => void refreshProject(false)} disabled={!selectedProject || loading || isDemo}><RefreshCwIcon /></Button>
      <Button variant="ghost" size="icon" title="Remove project from viewer" aria-label="Remove project from viewer" onclick={() => void removeProject()} disabled={!selectedProject || loading || isDemo}><Trash2Icon /></Button>
    </div>
  </header>

  <div class="status-region" aria-live="polite">
    {#if message}<span>{message}</span>{/if}
  </div>

  {#if error}
    <main class="center-state">
      <div class="state-symbol error-symbol" aria-hidden="true">!</div>
      <p class="eyebrow">Project unavailable</p>
      <h1>We cannot read this project.</h1>
      <p>{error}</p>
      <div class="state-actions">
        <Button onclick={() => selectedProject ? void refreshProject(false) : void initialize()}>Try again</Button>
        <Button variant="outline" onclick={() => void addProject(true)}>Choose its new location</Button>
      </div>
    </main>
  {:else if selectedId === "__overview__"}
    <main class="dashboard overview-dashboard">
      <section class="overview-heading">
        <div>
          <p class="eyebrow">Project overview</p>
          <h1>Where the work stands.</h1>
          <p>Open a project to inspect its Plan points and Decisions. Removing an entry here never changes the project files.</p>
        </div>
        <Button size="lg" onclick={() => void addProject()} disabled={loading}><PlusIcon /> Add project</Button>
      </section>
      <section class="project-cards" aria-label="Saved projects" aria-busy={loading}>
        {#each overviewEntries as entry (entry.project.id)}
          {@const overviewPlan = entry.snapshot?.plans.find((plan) => plan.id === entry.snapshot?.active_plan) ?? null}
          {@const overviewItem = overviewPlan?.work_items.find((item) => item.id === overviewPlan.current_item) ?? null}
          {@const overviewProgress = summarizeWork(overviewPlan?.work_items ?? [])}
          <article class="project-card" class:unavailable={Boolean(entry.error)}>
            <div class="project-card-head">
              <span class="project-initial" aria-hidden="true">{entry.project.name.slice(0, 1).toUpperCase()}</span>
              <div><h2>{entry.project.name}</h2><p title={entry.project.path}>{entry.project.path}</p></div>
              <Button class="card-remove" variant="ghost" size="icon-sm" aria-label={`Remove ${entry.project.name} from viewer`} onclick={() => void removeProject(entry.project.id)} disabled={isDemo}><Trash2Icon /></Button>
            </div>
            {#if entry.error}
              <div class="project-error"><strong>Project unavailable</strong><span>{entry.error}</span></div>
              <div class="project-card-actions">
                <Button variant="outline" onclick={() => void relocateProject(entry.project.id)}>Choose new location</Button>
              </div>
            {:else if overviewPlan}
              <div class="project-plan-status">
                <Badge variant="secondary" class="status-pill {overviewItem?.status ?? "todo"}">{overviewItem ? workStatusLabel(overviewItem.status) : "Selected"}</Badge>
                <small>{overviewPlan.id}</small>
                <strong>{overviewItem?.title ?? overviewPlan.title}</strong>
                <p>{overviewItem?.next_action ?? overviewPlan.goal}</p>
              </div>
              <div class="project-card-foot">
                <span>{overviewProgress.done} completed · {overviewProgress.todo} upcoming</span>
                <Button variant="outline" onclick={() => void selectProject(entry.project.id)}>Open project</Button>
              </div>
            {:else}
              <div class="project-plan-status idle"><Badge variant="secondary" class="status-pill todo">Idle</Badge><strong>No active Plan</strong><p>Open the project to inspect its retained Plan and Decision history.</p></div>
              <div class="project-card-foot"><span>{entry.snapshot?.plans.length ?? 0} retained Plans</span><Button variant="outline" onclick={() => void selectProject(entry.project.id)}>Open project</Button></div>
            {/if}
          </article>
        {/each}
      </section>
    </main>
  {:else if loading && !snapshot}
    <main class="center-state loading-state" aria-busy="true">
      <div class="loader" aria-hidden="true"></div>
      <h1>Reading project</h1>
      <p>Checking the index, Plans, Work Items, and Decisions…</p>
    </main>
  {:else if !snapshot}
    <main class="center-state empty-state">
      <div class="state-symbol" aria-hidden="true"><span></span><span></span><span></span></div>
      <p class="eyebrow">Local and read-only</p>
      <h1>Make project direction visible.</h1>
      <p>Choose a folder that contains <code>PROJECT_INDEX.md</code>, <code>docs/plans</code>, and <code>docs/decisions</code>.</p>
      <Button size="lg" onclick={() => void addProject()}><PlusIcon /> Add your first project</Button>
    </main>
  {:else}
    <main class="dashboard">
      <section class="project-heading" aria-labelledby="project-title">
        <div>
          <p class="project-name">{snapshot.name}</p>
          <p class="eyebrow">{selectedPlan?.status === "active" ? `Active Plan · ${selectedPlan.id}` : selectedPlan ? `Plan history · ${selectedPlan.id}` : "Project idle"}</p>
          <h1 id="project-title">{selectedPlan?.title ?? snapshot.name}</h1>
          {#if selectedPlan}
            <Collapsible.Root class="plan-goal">
              <Collapsible.Trigger class="plan-goal-summary">
                <strong>Plan goal</strong>
                <ChevronDownIcon class="disclosure" aria-hidden="true" />
              </Collapsible.Trigger>
              <Collapsible.Content class="plan-goal-content">
                <p class="project-goal">{selectedPlan.goal}</p>
              </Collapsible.Content>
            </Collapsible.Root>
          {:else}
            <p class="project-goal">This project currently has no active Plan.</p>
          {/if}
        </div>
      </section>

      {#if selectedPlan?.status === "active" && currentItem}
        <section class="current-card" aria-labelledby="current-title">
          <div class="current-index" aria-hidden="true">{stepNumber(selectedPlan.work_items.findIndex((item) => item.id === currentItem.id), selectedPlan.work_items.length)}</div>
          <div class="current-main">
            <div class="current-meta">
              <Badge variant={currentItem.status === "in_progress" ? "default" : "secondary"} class="status-pill {currentItem.status}">{workStatusLabel(currentItem.status)}</Badge>
              <span>Current Plan point · {currentItem.id}</span>
            </div>
            <h2 id="current-title">{currentItem.title}</h2>
            <p>{currentItem.outcome}</p>
          </div>
          <div class="next-action">
            <span>Next action</span>
            <strong>{currentItem.next_action}</strong>
          </div>
          {#if currentItem.blocked_by.length}
            <div class="blocker"><span>Blocked by</span><strong>{currentItem.blocked_by.join(", ")}</strong></div>
          {/if}
        </section>
      {/if}

      <section class="progress-band" aria-label="Plan progress">
        <div class="progress-copy">
          <strong>{progress.done} completed</strong>
          <span>{progress.in_progress} in progress</span>
          <span>{progress.paused} paused</span>
          <span>{progress.todo} upcoming</span>
          {#if progress.cancelled}<span>{progress.cancelled} cancelled</span>{/if}
        </div>
        <div class="progress-track" aria-hidden="true">
          {#if selectedPlan?.work_items.length}
            <span class="done" style:width={`${(progress.done / selectedPlan.work_items.length) * 100}%`}></span>
            <span class="active" style:width={`${(progress.in_progress / selectedPlan.work_items.length) * 100}%`}></span>
            <span class="paused" style:width={`${(progress.paused / selectedPlan.work_items.length) * 100}%`}></span>
            <span class="cancelled" style:width={`${(progress.cancelled / selectedPlan.work_items.length) * 100}%`}></span>
          {/if}
        </div>
      </section>

      <Tabs.Root bind:value={compactPane} class="compact-tabs">
        <Tabs.List variant="line" aria-label="Project information">
          <Tabs.Trigger id="plan-tab" aria-controls="plan-panel" value="plan">Plan</Tabs.Trigger>
          <Tabs.Trigger id="decisions-tab" aria-controls="decisions-panel" value="decisions">Decisions</Tabs.Trigger>
        </Tabs.List>
      </Tabs.Root>

      <div class="content-grid">
        <div id="plan-panel" role="tabpanel" class="pane plan-pane" class:compact-hidden={compactPane !== "plan"} aria-labelledby="plan-tab">
          <div class="section-heading">
            <div><p class="eyebrow">Ordered work</p><h2 id="work-heading">Plan points</h2></div>
            <div class="filter-row" aria-label="Filter plan points">
              {#each [["all", "All"], ["in_progress", "Active"], ["todo", "Upcoming"], ["done", "Completed"], ["blocked", "Blocked"]] as option}
                <Button size="sm" aria-pressed={workFilter === option[0]} variant={workFilter === option[0] ? "default" : "ghost"} onclick={() => selectWorkFilter(option[0] as typeof workFilter)}>{option[1]}</Button>
              {/each}
            </div>
          </div>

          <div class="work-list">
            {#if visibleItems.length > PAGE_SIZE}
              <Pagination itemLabel="Plan point" page={workPage} pageCount={workPageCount} pageSize={PAGE_SIZE} placement="top" total={visibleItems.length} onSelect={(page) => void selectPage("work", page)} />
            {/if}
            {#each pagedItems as item, index (item.id)}
              <Collapsible.Root class="work-item {item.status}" open={openWorkItems.has(item.id)} onOpenChange={(open) => setWorkItemOpen(item.id, open)}>
                <Collapsible.Trigger class="work-summary">
                  <span class="step-number">{stepNumber(selectedPlan?.work_items.indexOf(item) ?? index, selectedPlan?.work_items.length ?? 0)}</span>
                  <span class="timeline-marker" aria-hidden="true">
                    {#if item.status === "done"}✓
                    {:else if item.status === "paused"}<PauseIcon />
                    {:else if item.status === "cancelled"}<XIcon />
                    {:else if item.status === "in_progress"}<PlayIcon />
                    {:else}<CircleIcon />
                    {/if}
                  </span>
                  <span class="item-title"><small>{item.id} · {workStatusLabel(item.status)}</small><strong>{item.title}</strong></span>
                  {#if item.status === "paused" || item.status === "cancelled" || item.blocked_by.length}
                    <span class="work-labels">
                      {#if item.status === "paused"}<Badge variant="secondary" class="status-pill paused">Paused</Badge>{/if}
                      {#if item.status === "cancelled"}<Badge variant="secondary" class="status-pill cancelled">Cancelled</Badge>{/if}
                      {#if item.blocked_by.length}<Badge variant="secondary" class="blocked-label">Blocked</Badge>{/if}
                    </span>
                  {/if}
                  <ChevronDownIcon class="disclosure" aria-hidden="true" />
                </Collapsible.Trigger>
                <Collapsible.Content class="item-detail">
                  <p>{item.outcome}</p>
                  {#if item.next_action}<div class="detail-callout"><span>Next action</span><strong>{item.next_action}</strong></div>{/if}
                  <dl>
                    <div><dt>Acceptance</dt><dd>{item.acceptance}</dd></div>
                    {#if item.steps.length}
                      <div>
                        <dt>Steps</dt>
                        <dd>
                          <ol class="work-steps">
                            {#each item.steps as step}
                              <li>{step}</li>
                            {/each}
                          </ol>
                        </dd>
                      </div>
                    {/if}
                    {#if item.depends_on.length}<div><dt>Depends on</dt><dd>{item.depends_on.join(", ")}</dd></div>{/if}
                    {#if item.blocked_by.length}<div><dt>Blocked by</dt><dd>{item.blocked_by.join(", ")}</dd></div>{/if}
                    {#if item.decisions.length}<div><dt>Decisions</dt><dd>{item.decisions.join(", ")}</dd></div>{/if}
                    {#if item.evidence.length}<div><dt>Evidence</dt><dd>{item.evidence.join(" · ")}</dd></div>{/if}
                  </dl>
                </Collapsible.Content>
              </Collapsible.Root>
            {:else}
              <p class="inline-empty">No Plan points match this filter.</p>
            {/each}
            {#if visibleItems.length > PAGE_SIZE}
              <Pagination itemLabel="Plan point" page={workPage} pageCount={workPageCount} pageSize={PAGE_SIZE} placement="bottom" total={visibleItems.length} onSelect={(page) => void selectPage("work", page)} />
            {/if}
          </div>
        </div>

        <div id="decisions-panel" role="tabpanel" class="pane decisions-pane" class:compact-hidden={compactPane !== "decisions"} aria-labelledby="decisions-tab">
          <div class="section-heading">
            <div><p class="eyebrow">Project direction</p><h2 id="decision-heading">Decisions</h2></div>
          </div>
          <div class="decision-filters" aria-label="Filter decisions">
            {#each [["current", "Current"], ["proposed", "Proposed"], ["history", "History"], ["all", "All"]] as option}
              <Button size="sm" aria-pressed={decisionFilter === option[0]} variant={decisionFilter === option[0] ? "default" : "ghost"} onclick={() => selectDecisionFilter(option[0] as typeof decisionFilter)}>{option[1]}</Button>
            {/each}
          </div>

          <div class="decision-list">
            {#if visibleDecisions.length > PAGE_SIZE}
              <Pagination itemLabel="Decision" page={decisionPage} pageCount={decisionPageCount} pageSize={PAGE_SIZE} placement="top" total={visibleDecisions.length} onSelect={(page) => void selectPage("decision", page)} />
            {/if}
            {#each pagedDecisions as decision (decision.id)}
              <Collapsible.Root class="decision-item {decision.status}" open={openDecisions.has(decision.id)} onOpenChange={(open) => setDecisionOpen(decision.id, open)}>
                <Collapsible.Trigger class="decision-summary">
                  <span class="decision-status" aria-hidden="true"></span>
                  <span><small>{decision.id} · {decisionStatusLabel(decision.status)} · {decision.scope}</small><strong>{decision.title}</strong></span>
                  <ChevronDownIcon class="disclosure" aria-hidden="true" />
                </Collapsible.Trigger>
                <Collapsible.Content class="decision-detail">
                  <p>{decision.decision}</p>
                  {#if decision.superseded_by}
                    <div class="supersession"><span>Replaced by</span><strong>{decision.superseded_by} · {decisionById(decision.superseded_by)?.title ?? "Decision not found"}</strong></div>
                  {:else if decision.supersedes}
                    <div class="supersession"><span>Replaces</span><strong>{decision.supersedes} · {decisionById(decision.supersedes)?.title ?? "Decision not found"}</strong></div>
                  {/if}
                  <dl>
                    <div><dt>Status</dt><dd>{decisionStatusLabel(decision.status)}{decision.status === "accepted" ? " · accepted and currently applicable" : ""}</dd></div>
                    <div><dt>Active Plan point</dt><dd>{linkedDecisionIds.has(decision.id) && activeCurrentItem ? `Linked to ${activeCurrentItem.id}` : "Not linked"}</dd></div>
                    <div><dt>Consequences</dt><dd>{decision.consequences}</dd></div>
                    <div><dt>Revisit when</dt><dd>{decision.revisit_when}</dd></div>
                  </dl>
                </Collapsible.Content>
              </Collapsible.Root>
            {:else}
              <p class="inline-empty">No Decisions match this filter.</p>
            {/each}
            {#if visibleDecisions.length > PAGE_SIZE}
              <Pagination itemLabel="Decision" page={decisionPage} pageCount={decisionPageCount} pageSize={PAGE_SIZE} placement="bottom" total={visibleDecisions.length} onSelect={(page) => void selectPage("decision", page)} />
            {/if}
          </div>
        </div>
      </div>
    </main>
  {/if}
</div>
