import { useEffect, useState } from 'react';
import type { HealthCheckResponse } from '@dsa-studio/shared';
import { apiClient } from '@/lib/api-client';

interface HealthState {
  data: HealthCheckResponse | null;
  loading: boolean;
  error: string | null;
}

export function useHealthCheck(): HealthState {
  const [data, setData] = useState<HealthCheckResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    apiClient
      .getHealth()
      .then((health) => {
        if (!cancelled) {
          setData(health);
          setError(null);
        }
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Failed to reach API');
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return { data, loading, error };
}
