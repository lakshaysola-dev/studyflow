import { Card, CardTitle } from "@/components/ui/card";
import type { TagMinutes } from "@/lib/types";
import { formatMinutes } from "@/lib/utils";

export function BlockSystem({ data }: { data: TagMinutes[] }) {
  const total = data.reduce((acc, t) => acc + t.minutes, 0);

  return (
    <Card>
      <div className="mb-4 flex items-center justify-between">
        <CardTitle>Block System</CardTitle>
        <span className="text-xs text-muted-foreground">{formatMinutes(total)} planned</span>
      </div>
      {total === 0 ? (
        <p className="text-sm text-muted-foreground">
          Time-block your day with tags like Deep Work, Lectures and Relaxation.
        </p>
      ) : (
        <>
          <div className="flex h-3 w-full overflow-hidden rounded-full bg-muted">
            {data.map((t) => (
              <div
                key={t.tag_name}
                style={{ width: `${(t.minutes / total) * 100}%`, backgroundColor: t.color }}
                title={`${t.tag_name}: ${formatMinutes(t.minutes)}`}
              />
            ))}
          </div>
          <ul className="mt-4 space-y-2">
            {data.map((t) => (
              <li key={t.tag_name} className="flex items-center justify-between text-sm">
                <span className="flex items-center gap-2">
                  <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: t.color }} />
                  {t.tag_name}
                </span>
                <span className="tabular-nums text-muted-foreground">
                  {formatMinutes(t.minutes)}
                </span>
              </li>
            ))}
          </ul>
        </>
      )}
    </Card>
  );
}
