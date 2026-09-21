import { loadResults } from "../../lib/data";
import ReviewQueueClient from "../../components/ReviewQueueClient";

export const dynamic = "force-dynamic";

export const metadata = {
  title: "ShipCheck — Review Queue",
  description: "Human-in-the-loop review queue for shipping document verification",
};

export default async function ReviewPage() {
  const results = await loadResults();
  const reviewCases = results.filter(
    (r) => r.status === "NEEDS_REVIEW" || r.status === "FAIL"
  );

  return <ReviewQueueClient cases={reviewCases} />;
}
