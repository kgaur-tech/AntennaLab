import type { RecommendationCandidate } from '../types';

interface AntennaRecommendationsProps {
  items: RecommendationCandidate[];
}

export default function AntennaRecommendations({ items }: AntennaRecommendationsProps) {
  if (!items.length) {
    return <p>No recommendation available yet.</p>;
  }

  return (
    <ul>
      {items.map((candidate) => (
        <li key={candidate.family} style={{ marginBottom: '1rem' }}>
          <strong>{candidate.family}</strong> — score {candidate.score.toFixed(2)}
          <ul>
            {candidate.reasons.map((reason) => (
              <li key={reason}>{reason}</li>
            ))}
          </ul>
        </li>
      ))}
    </ul>
  );
}
