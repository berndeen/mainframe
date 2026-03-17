import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

interface CTAProps {
  ctaText: string;
  accentColor: string;
}

export const CTA: React.FC<CTAProps> = ({ ctaText, accentColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 10, stiffness: 150 } });
  const opacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Pulsing glow effect after entrance
  const pulseFrame = Math.max(0, frame - 30);
  const pulse = 1 + Math.sin(pulseFrame * 0.15) * 0.03;

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          transform: `scale(${scale * pulse})`,
          opacity,
          padding: '28px 64px',
          backgroundColor: accentColor,
          borderRadius: 60,
          fontSize: 36,
          fontWeight: 700,
          letterSpacing: 2,
          textTransform: 'uppercase',
          boxShadow: `0 0 40px ${accentColor}66`,
        }}
      >
        {ctaText}
      </div>
    </AbsoluteFill>
  );
};
