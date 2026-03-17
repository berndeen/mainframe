import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';

interface BodyLineSceneProps {
  line: string;
  index: number;
  total: number;
}

export const BodyLineScene: React.FC<BodyLineSceneProps> = ({ line, index, total }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 15, stiffness: 200 } });
  const translateY = interpolate(entrance, [0, 1], [60, 0]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);

  // Progress indicator
  const progress = (index + 1) / total;

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
        padding: 80,
      }}
    >
      <div
        style={{
          fontSize: 44,
          fontWeight: 600,
          textAlign: 'center',
          transform: `translateY(${translateY}px)`,
          opacity,
          lineHeight: 1.4,
          textShadow: '0 2px 12px rgba(0,0,0,0.2)',
        }}
      >
        {line}
      </div>

      {/* Progress dots */}
      <div
        style={{
          position: 'absolute',
          bottom: 120,
          display: 'flex',
          gap: 12,
          opacity: interpolate(frame, [5, 15], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        {Array.from({ length: total }).map((_, i) => (
          <div
            key={i}
            style={{
              width: 12,
              height: 12,
              borderRadius: '50%',
              backgroundColor: i <= index ? '#FFFFFF' : 'rgba(255,255,255,0.3)',
              transition: 'none',
            }}
          />
        ))}
      </div>
    </AbsoluteFill>
  );
};
