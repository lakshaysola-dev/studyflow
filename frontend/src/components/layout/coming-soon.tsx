import { Card } from "@/components/ui/card";
import { PageHeader } from "./page-header";

export function ComingSoon({
  title,
  phase,
  description,
}: {
  title: string;
  phase: number;
  description: string;
}) {
  return (
    <>
      <PageHeader title={title} />
      <Card className="flex flex-col items-center justify-center py-20 text-center">
        <span className="mb-3 rounded-full bg-primary/15 px-3 py-1 text-xs font-medium text-primary">
          Phase {phase}
        </span>
        <p className="max-w-md text-sm text-muted-foreground">{description}</p>
      </Card>
    </>
  );
}
