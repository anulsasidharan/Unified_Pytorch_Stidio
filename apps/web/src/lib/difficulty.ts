import type { Difficulty } from '@dsa-studio/shared';

export function difficultyVariant(
  difficulty: string,
): 'basic' | 'intermediate' | 'advanced' | 'default' {
  if (difficulty === 'basic' || difficulty === 'intermediate' || difficulty === 'advanced') {
    return difficulty;
  }
  return 'default';
}

export function progressIcon(status?: string): string {
  switch (status) {
    case 'solved':
    case 'mastered':
      return '✅';
    case 'attempted':
      return '❌';
    default:
      return '⭕';
  }
}

export const DIFFICULTY_LABELS: Record<Difficulty, string> = {
  basic: 'Basic',
  intermediate: 'Intermediate',
  advanced: 'Advanced',
};
