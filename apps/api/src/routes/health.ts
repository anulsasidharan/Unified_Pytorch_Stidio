import { Router } from 'express';
import type { ApiSuccessResponse, HealthCheckResponse } from '@dsa-studio/shared';

export const healthRouter = Router();

healthRouter.get('/health', (_req, res) => {
  const payload: ApiSuccessResponse<HealthCheckResponse> = {
    success: true,
    data: {
      status: 'ok',
      service: 'dsa-studio-api',
      version: '0.1.0',
      timestamp: new Date().toISOString(),
    },
  };

  res.json(payload);
});
