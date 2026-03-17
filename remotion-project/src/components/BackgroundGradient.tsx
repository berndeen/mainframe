import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

interface BackgroundGradientProps {
  from: string;
  to: string;
  angle?: number;
  animated?: boolean;
  children?: React.ReactNode;
}

export const BackgroundGradient: React.FC<BackgroundGradientProps> = ({
  from,
  to,
  angle = 135,
  animated = false,
  children,
}) => {
  const frame = useCurrentFrame();

  const currentAngle = animated
    ? angle + interpolate(frame, [0, 300], [0, 360], { extrapolateRight: 'extend' })
    : angle;

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(${currentAngle}deg, ${from}, ${to})`,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};
