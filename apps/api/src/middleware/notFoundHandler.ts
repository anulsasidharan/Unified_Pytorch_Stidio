import type { NextFunction, Request, Response } from 'express';
import { AppError, toErrorResponse } from './errorHandler.js';

export function notFoundHandler(_req: Request, _res: Response, next: NextFunction): void {
  next(new AppError(404, 'NOT_FOUND', 'Route not found'));
}

export function errorHandler(
  error: unknown,
  _req: Request,
  res: Response,
  _next: NextFunction,
): void {
  const statusCode = error instanceof AppError ? error.statusCode : 500;
  res.status(statusCode).json(toErrorResponse(error));
}
