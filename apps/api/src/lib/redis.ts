interface Bucket {
  count: number;
  expiresAt: number;
}

const buckets = new Map<string, Bucket>();

export async function checkRateLimit(
  key: string,
  limit: number,
  windowSeconds: number,
): Promise<{ allowed: boolean; remaining: number; retryAfter: number }> {
  const now = Date.now();
  const existing = buckets.get(key);

  if (!existing || existing.expiresAt <= now) {
    const expiresAt = now + windowSeconds * 1000;
    buckets.set(key, { count: 1, expiresAt });
    return { allowed: true, remaining: limit - 1, retryAfter: windowSeconds };
  }

  existing.count += 1;
  const ttl = Math.max(1, Math.ceil((existing.expiresAt - now) / 1000));

  return {
    allowed: existing.count <= limit,
    remaining: Math.max(0, limit - existing.count),
    retryAfter: ttl,
  };
}
