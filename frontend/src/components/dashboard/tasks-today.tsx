import { formatInTimeZone } from "date-fns-tz";
import { Card, CardTitle } from "@/components/ui/card";
import type { TaskSummary } from "@/lib/types";
import { cn } from "@/lib/utils";

function quadrant(t: TaskSummary) {
  if (t.is_urgent && t.is_important) return { label: "Do", className: "bg-red-500/15 text-red-400" };
  if (t.is_important) return { label: "Plan", className: "bg-blue-500/15 text-blue-400" };
  if (t.is_urgent) return { label: "Delegate", className: "bg-amber-500/15 text-amber-400" };
  return { label: "Later", className: "bg-zinc-500/15 text-zinc-400" };
}

export function TasksToday({ tasks, timezone }: { tasks: TaskSummary[]; timezone: string }) {
  return (
    <Card>
      <div className="mb-4 flex items-center justify-between">
        <CardTitle>Due Today</CardTitle>
        <span className="text-xs text-muted-foreground">{tasks.length} open</span>
      </div>
      {tasks.length === 0 ? (
        <p className="text-sm text-muted-foreground">Nothing due today. Nice.</p>
      ) : (
        <ul className="space-y-2">
          {tasks.map((t) => {
            const q = quadrant(t);
            return (
              <li
                key={t.id}
                className="flex items-center justify-between gap-3 rounded-lg bg-muted/60 px-3 py-2 text-sm"
              >
                <span className="truncate">{t.title}</span>
                <span className="flex shrink-0 items-center gap-2 text-xs text-muted-foreground">
                  {t.due_at && formatInTimeZone(t.due_at, timezone, "h:mm a")}
                  <span className={cn("rounded px-1.5 py-0.5 font-medium", q.className)}>
                    {q.label}
                  </span>
                </span>
              </li>
            );
          })}
        </ul>
      )}
    </Card>
  );
}
