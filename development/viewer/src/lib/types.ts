export type PlanStatus = "draft" | "active" | "completed" | "cancelled";
export type WorkStatus = "todo" | "in_progress" | "paused" | "done" | "cancelled";
export type DecisionStatus = "proposed" | "accepted" | "rejected" | "deprecated" | "superseded";

export interface WorkItem {
  id: string;
  title: string;
  status: WorkStatus;
  depends_on: string[];
  blocked_by: string[];
  decisions: string[];
  outcome: string;
  acceptance: string;
  steps: string[];
  evidence: string[];
  next_action: string | null;
}

export interface Plan {
  id: string;
  title: string;
  status: PlanStatus;
  created: string;
  updated: string;
  current_item: string | null;
  goal: string;
  non_goals: string;
  work_items: WorkItem[];
  source_path: string;
}

export interface Decision {
  id: string;
  title: string;
  status: DecisionStatus;
  created: string;
  accepted: string | null;
  scope: string;
  supersedes: string | null;
  superseded_by: string | null;
  decision: string;
  problem: string;
  consequences: string;
  revisit_when: string;
  source_path: string;
}

export interface ProjectSnapshot {
  root: string;
  name: string;
  active_plan: string | null;
  plans: Plan[];
  decisions: Decision[];
  loaded_at: number;
}

export interface SavedProject {
  id: string;
  name: string;
  path: string;
}

export interface ProjectRegistry {
  version: number;
  selected: string;
  projects: SavedProject[];
}
