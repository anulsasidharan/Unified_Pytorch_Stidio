import type { NextFunction, Response } from 'express';
import { checkRateLimit } from '../lib/redis.js';
import { AppError } from './errorHandler.js';
import type { AuthenticatedRequest } from './auth.js';

export interface RateLimitOptions {
  keyPrefix: string;
  limit: number;
  windowSeconds?: number;
}

export function rateLimit(options: RateLimitOptions) {
  const windowSeconds = options.windowSeconds ?? 3600;

  return async (req: AuthenticatedRequest, _res: Response, next: NextFunction): Promise<void> => {
    try {
      const userId = req.userId ?? req.ip ?? 'anonymous';
      const key = `${options.keyPrefix}:${userId}`;
      const result = await checkRateLimit(key, options.limit, windowSeconds);

      if (!result.allowed) {
        next(
          new AppError(
            429,
            'RATE_LIMIT_EXCEEDED',
            `Rate limit exceeded. Try again in ${result.retryAfter} seconds.`,
            { retryAfter: result.retryAfter },
          ),
        );
        return;
      }

      next();
    } catch (error) {
      next(error);
    }
  };
}
