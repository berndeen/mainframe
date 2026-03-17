import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

interface FeaturesProps {
  features: Array<{ icon: string; label: string }>;
  accentColor: string;
}

export const Features: React.FC<FeaturesProps> = ({ features, accentColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
        padding: 60,
      }}
    >
      <div
        style={{
          fontSize: 42,
          fontWeight: 700,
          marginBottom: 60,
          opacity: interpolate(frame, [0, 15], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        Features
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 30, width: '100%' }}>
        {features.map((feature, i) => {
          const delay = 10 + i * 10;
          const s = spring({ frame, fps, delay, config: { damping: 14, stiffness: 180 } });
          const translateX = interpolate(s, [0, 1], [80, 0]);
          const opacity = interpolate(s, [0, 1], [0, 1]);

          return (
            <div
              key={i}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 24,
                padding: '20px 30px',
                backgroundColor: 'rgba(255, 255, 255, 0.08)',
                borderRadius: 16,
                borderLeft: `4px solid ${accentColor}`,
                transform: `translateX(${translateX}px)`,
                opacity,
              }}
            >
              <span style={{ fontSize: 48 }}>{feature.icon}</span>
              <span style={{ fontSize: 28, fontWeight: 500 }}>{feature.label}</span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
