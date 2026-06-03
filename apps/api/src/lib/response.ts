import type { ApiSuccessResponse, PaginatedMeta } from '@dsa-studio/shared';

export function success<T>(data: T): ApiSuccessResponse<T> {
  return { success: true, data };
}

export function paginatedMeta(page: number, limit: number, total: number): PaginatedMeta {
  return {
    page,
    limit,
    total,
    totalPages: Math.ceil(total / limit) || 0,
  };
}
