import { interpolate, spring } from 'remotion';

/**
 * Fade in over a given number of frames, clamped.
 */
export function fadeIn(frame: number, duration: number = 30): number {
  return interpolate(frame, [0, duration], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
}

/**
 * Fade out over a given number of frames, starting at `startFrame`.
 */
export function fadeOut(
  frame: number,
  startFrame: number,
  duration: number = 30,
): number {
  return interpolate(frame, [startFrame, startFrame + duration], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
}

/**
 * Slide in from a direction with spring physics.
 */
export function slideIn(
  frame: number,
  fps: number,
  direction: 'left' | 'right' | 'up' | 'down',
  distance: number = 100,
  delay: number = 0,
): number {
  const s = spring({ frame, fps, delay, config: { damping: 15, stiffness: 180 } });
  const sign = direction === 'right' || direction === 'down' ? 1 : -1;
  return interpolate(s, [0, 1], [sign * distance, 0]);
}

/**
 * Scale entrance with spring.
 */
export function scaleIn(
  frame: number,
  fps: number,
  delay: number = 0,
): number {
  return spring({
    frame,
    fps,
    delay,
    config: { damping: 12, stiffness: 200, mass: 0.5 },
  });
}
