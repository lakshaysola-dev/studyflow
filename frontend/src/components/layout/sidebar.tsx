"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BarChart3,
  CalendarDays,
  CheckSquare,
  Inbox,
  LayoutDashboard,
  LogOut,
  Settings,
  Target,
  Timer,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useLogout, useMe } from "@/hooks/use-auth";

const NAV = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/calendar", label: "Calendar", icon: CalendarDays },
  { href: "/tasks", label: "Tasks", icon: CheckSquare },
  { href: "/goals", label: "Goals", icon: Target },
  { href: "/focus", label: "Focus", icon: Timer },
  { href: "/stats", label: "Stats", icon: BarChart3 },
  { href: "/inbox", label: "Inbox", icon: Inbox },
];

export function Sidebar() {
  const pathname = usePathname();
  const { data: user } = useMe();
  const logout = useLogout();

  return (
    <aside className="flex h-screen w-60 shrink-0 flex-col border-r bg-card/60">
      <div className="flex items-center gap-2 px-5 py-5">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-sm font-bold text-primary-foreground">
          S
        </div>
        <span className="text-lg font-semibold tracking-tight">StudyFlow</span>
      </div>
      <nav className="flex-1 space-y-1 px-3">
        {NAV.map(({ href, label, icon: Icon }) => {
          const active = href === "/" ? pathname === "/" : pathname.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors",
                active
                  ? "bg-primary/15 text-foreground"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground",
              )}
            >
              <Icon className={cn("h-4 w-4", active && "text-primary")} />
              {label}
            </Link>
          );
        })}
      </nav>
      <div className="border-t p-3">
        <Link
          href="/settings"
          className={cn(
            "flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-foreground",
            pathname.startsWith("/settings") && "bg-primary/15 text-foreground",
          )}
        >
          <Settings className="h-4 w-4" />
          Settings
        </Link>
        <div className="mt-2 flex items-center justify-between rounded-lg px-3 py-2">
          <div className="min-w-0">
            <p className="truncate text-sm font-medium">{user?.full_name || "Student"}</p>
            <p className="truncate text-xs text-muted-foreground">{user?.email}</p>
          </div>
          <button
            onClick={logout}
            className="rounded-md p-1.5 text-muted-foreground hover:bg-muted hover:text-foreground"
            aria-label="Log out"
          >
            <LogOut className="h-4 w-4" />
          </button>
        </div>
      </div>
    </aside>
  );
}
