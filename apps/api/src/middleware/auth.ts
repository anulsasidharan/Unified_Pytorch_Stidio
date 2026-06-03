import type { NextFunction, Request, Response } from 'express';
import { AppError } from './errorHandler.js';
import { verifyToken } from '../lib/jwt.js';
import { prisma } from '../lib/prisma.js';

export interface AuthenticatedRequest extends Request {
  userId?: string;
}

export async function requireAuth(
  req: AuthenticatedRequest,
  _res: Response,
  next: NextFunction,
): Promise<void> {
  try {
    const header = req.headers.authorization;
    if (!header?.startsWith('Bearer ')) {
      throw new AppError(401, 'UNAUTHORIZED', 'Authentication required');
    }

    const token = header.slice(7);
    const payload = verifyToken(token);

    const user = await prisma.user.findUnique({ where: { userId: payload.userId } });
    if (!user) {
      throw new AppError(401, 'UNAUTHORIZED', 'Invalid or expired token');
    }

    req.userId = payload.userId;
    next();
  } catch (error) {
    if (error instanceof AppError) {
      next(error);
      return;
    }
    next(new AppError(401, 'UNAUTHORIZED', 'Invalid or expired token'));
  }
}

export function optionalAuth(
  req: AuthenticatedRequest,
  _res: Response,
  next: NextFunction,
): void {
  const header = req.headers.authorization;
  if (!header?.startsWith('Bearer ')) {
    next();
    return;
  }

  try {
    const payload = verifyToken(header.slice(7));
    req.userId = payload.userId;
  } catch {
    // Ignore invalid tokens for optional auth
  }

  next();
}
