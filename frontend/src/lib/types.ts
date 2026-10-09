export interface User {
  id: string;
  email: string;
  full_name: string;
  timezone: string;
  focus_minutes: number;
  short_break_minutes: number;
  long_break_minutes: number;
  daily_focus_goal_minutes: number;
  created_at: string;
}

export interface Token {
  access_token: string;
  token_type: string;
  user: User;
}

export interface BlockSummary {
  id: string;
  title: string;
  start_at: string;
  end_at: string;
  tag_name: string | null;
  tag_color: string | null;
}

export interface TaskSummary {
  id: string;
  title: string;
  status: string;
  is_urgent: boolean;
  is_important: boolean;
  due_at: string | null;
}

export interface TagMinutes {
  tag_name: string;
  color: string;
  minutes: number;
}

export interface DashboardStats {
  focus_minutes_today: number;
  focus_goal_minutes: number;
  tasks_due_today: number;
  tasks_completed_today: number;
  attendance_percentage: number | null;
  low_attendance_courses: number;
  minutes_by_tag_today: TagMinutes[];
}

export interface DashboardSummary {
  date: string;
  greeting: string;
  stats: DashboardStats;
  blocks_today: BlockSummary[];
  tasks_today: TaskSummary[];
}
