"use client";

import { differenceInMinutes, format, startOfDay } from "date-fns";
import { toZonedTime } from "date-fns-tz";
import { useEffect, useState } from "react";
import { Card, CardTitle } from "@/components/ui/card";
import type { BlockSummary } from "@/lib/types";

const START_HOUR = 6;
const END_HOUR = 24;
const HOUR_HEIGHT = 56;
const HOURS = Array.from({ length: END_HOUR - START_HOUR }, (_, i) => START_HOUR + i);

function minutesFromStart(d: Date) {
  return differenceInMinutes(d, startOfDay(d)) - START_HOUR * 60;
}

export function DayPlanner({ blocks, timezone }: { blocks: BlockSummary[]; timezone: string }) {
  const [tick, setTick] = useState(() => Date.now());
  useEffect(() => {
    const id = setInterval(() => setTick(Date.now()), 60_000);
    return () => clearInterval(id);
  }, []);
  const now = toZonedTime(tick, timezone);

  const nowOffset = (minutesFromStart(now) / 60) * HOUR_HEIGHT;
  const showNow = nowOffset >= 0 && nowOffset <= (END_HOUR - START_HOUR) * HOUR_HEIGHT;

  return (
    <Card className="flex h-full flex-col">
      <div className="mb-4 flex items-center justify-between">
        <CardTitle>Day Planner</CardTitle>
        <span className="text-xs text-muted-foreground">{format(now, "EEEE, d MMM")}</span>
      </div>
      <div className="relative flex-1 overflow-y-auto pr-1" style={{ maxHeight: 560 }}>
        <div className="relative" style={{ height: HOURS.length * HOUR_HEIGHT }}>
          {HOURS.map((h) => (
            <div
              key={h}
              className="absolute left-0 right-0 flex border-t border-border/60"
              style={{ top: (h - START_HOUR) * HOUR_HEIGHT, height: HOUR_HEIGHT }}
            >
              <span className="-mt-2 w-12 shrink-0 text-[11px] text-muted-foreground">
                {format(new Date(2000, 0, 1, h), "h a")}
              </span>
            </div>
          ))}

          {blocks.map((b) => {
            const start = toZonedTime(b.start_at, timezone);
            const end = toZonedTime(b.end_at, timezone);
            const top = Math.max(0, (minutesFromStart(start) / 60) * HOUR_HEIGHT);
            const height = Math.max(
              22,
              (differenceInMinutes(end, start) / 60) * HOUR_HEIGHT - 2,
            );
            const color = b.tag_color ?? "#64748b";
            return (
              <div
                key={b.id}
                className="absolute left-14 right-2 overflow-hidden rounded-md border-l-2 px-2 py-1 text-xs"
                style={{
                  top,
                  height,
                  borderColor: color,
                  backgroundColor: `${color}22`,
                }}
              >
                <p className="truncate font-medium">{b.title}</p>
                <p className="truncate text-[11px] text-muted-foreground">
                  {format(start, "h:mm a")} – {format(end, "h:mm a")}
                  {b.tag_name ? ` · ${b.tag_name}` : ""}
                </p>
              </div>
            );
          })}

          {showNow && (
            <div className="absolute left-12 right-0 flex items-center" style={{ top: nowOffset }}>
              <span className="h-2 w-2 rounded-full bg-red-500" />
              <div className="h-px flex-1 bg-red-500/80" />
            </div>
          )}

          {blocks.length === 0 && (
            <div className="absolute inset-0 flex items-center justify-center">
              <p className="rounded-lg bg-card/80 px-4 py-2 text-sm text-muted-foreground">
                No blocks scheduled today. Add blocks from the Calendar (Phase 2).
              </p>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
}
