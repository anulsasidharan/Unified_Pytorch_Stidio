import { useCallback, useEffect, useState } from 'react';

export function useStepAnimation(stepCount: number, intervalMs = 2200, autoPlay = true) {
  const [step, setStep] = useState(0);
  const [playing, setPlaying] = useState(autoPlay);

  const next = useCallback(() => {
    setStep((s) => (s + 1) % stepCount);
  }, [stepCount]);

  const prev = useCallback(() => {
    setStep((s) => (s - 1 + stepCount) % stepCount);
  }, [stepCount]);

  const reset = useCallback(() => setStep(0), []);

  useEffect(() => {
    setStep(0);
    setPlaying(autoPlay);
  }, [stepCount, autoPlay]);

  useEffect(() => {
    if (!playing || stepCount <= 1) return;
    const id = window.setInterval(next, intervalMs);
    return () => window.clearInterval(id);
  }, [playing, stepCount, intervalMs, next]);

  return { step, playing, setPlaying, next, prev, reset };
}
