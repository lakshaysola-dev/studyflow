import type { LucideIcon } from "lucide-react";
import { Card, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export function StatCard({
  title,
  value,
  hint,
  icon: Icon,
  progress,
  accent = "text-primary",
}: {
  title: string;
  value: string;
  hint?: string;
  icon: LucideIcon;
  progress?: number;
  accent?: string;
}) {
  return (
    <Card>
      <div className="flex items-start justify-between">
        <CardTitle>{title}</CardTitle>
        <Icon className={cn("h-4 w-4", accent)} />
      </div>
      <p className="mt-3 text-3xl font-semibold tabular-nums">{value}</p>
      {hint && <p className="mt-1 text-xs text-muted-foreground">{hint}</p>}
      {progress !== undefined && (
        <div className="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-muted">
          <div
            className="h-full rounded-full bg-primary transition-all"
            style={{ width: `${Math.min(100, Math.max(0, progress))}%` }}
          />
        </div>
      )}
    </Card>
  );
}
