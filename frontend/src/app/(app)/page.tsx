"use client";

import { CheckCircle2, GraduationCap, Target, Timer } from "lucide-react";
import { BlockSystem } from "@/components/dashboard/block-system";
import { DayPlanner } from "@/components/dashboard/day-planner";
import { StatCard } from "@/components/dashboard/stat-card";
import { TasksToday } from "@/components/dashboard/tasks-today";
import { PageHeader } from "@/components/layout/page-header";
import { Card } from "@/components/ui/card";
import { useMe } from "@/hooks/use-auth";
import { useDashboard } from "@/hooks/use-dashboard";
import { formatMinutes } from "@/lib/utils";

export default function DashboardPage() {
  const { data, isLoading, error } = useDashboard();
  const { data: user } = useMe();
  const timezone = user?.timezone ?? Intl.DateTimeFormat().resolvedOptions().timeZone;

  if (isLoading) {
    return <p className="text-sm text-muted-foreground">Loading your day…</p>;
  }
  if (error || !data) {
    return (
      <Card className="border-red-500/40 text-sm text-red-400">
        Could not load dashboard: {error instanceof Error ? error.message : "unknown error"}
      </Card>
    );
  }

  const { stats } = data;
  const focusProgress = stats.focus_goal_minutes
    ? (stats.focus_minutes_today / stats.focus_goal_minutes) * 100
    : 0;
  const completionTotal = stats.tasks_due_today + stats.tasks_completed_today;
  const completion = completionTotal
    ? Math.round((stats.tasks_completed_today / completionTotal) * 100)
    : 0;

  return (
    <>
      <PageHeader title={data.greeting} subtitle="Here is how your day is shaping up." />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard
          title="Focus time"
          value={formatMinutes(stats.focus_minutes_today)}
          hint={`Goal ${formatMinutes(stats.focus_goal_minutes)}`}
          icon={Timer}
          progress={focusProgress}
        />
        <StatCard
          title="Daily goal"
          value={`${completion}%`}
          hint={`${stats.tasks_completed_today} of ${completionTotal} tasks done`}
          icon={CheckCircle2}
          progress={completion}
          accent="text-green-400"
        />
        <StatCard
          title="Attendance"
          value={stats.attendance_percentage === null ? "—" : `${stats.attendance_percentage}%`}
          hint={
            stats.attendance_percentage === null
              ? "Connect SLCM in Phase 5"
              : stats.low_attendance_courses
                ? `${stats.low_attendance_courses} course(s) below 75%`
                : "All courses above 75%"
          }
          icon={GraduationCap}
          accent="text-blue-400"
        />
        <StatCard
          title="Due today"
          value={String(stats.tasks_due_today)}
          hint="Open tasks with a deadline today"
          icon={Target}
          accent="text-amber-400"
        />
      </div>

      <div className="mt-6 grid grid-cols-1 gap-4 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <DayPlanner blocks={data.blocks_today} timezone={timezone} />
        </div>
        <div className="space-y-4">
          <BlockSystem data={stats.minutes_by_tag_today} />
          <TasksToday tasks={data.tasks_today} timezone={timezone} />
        </div>
      </div>
    </>
  );
}
