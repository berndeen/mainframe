import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { fadeIn, scaleIn, slideIn } from '../../../lib/animations';

interface IntroProps {
  title: string;
  subtitle?: string;
  accentColor: string;
}

export const Intro: React.FC<IntroProps> = ({ title, subtitle, accentColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleScale = scaleIn(frame, fps);
  const titleOpacity = fadeIn(frame, 20);
  const subtitleY = slideIn(frame, fps, 'up', 40, 15);
  const subtitleOpacity = fadeIn(frame - 15, 20);
  const lineWidth = fadeIn(frame - 5, 25);

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
          fontSize: 72,
          fontWeight: 800,
          textAlign: 'center',
          transform: `scale(${titleScale})`,
          opacity: titleOpacity,
          lineHeight: 1.1,
        }}
      >
        {title}
      </div>

      <div
        style={{
          width: `${lineWidth * 200}px`,
          height: 4,
          backgroundColor: accentColor,
          marginTop: 30,
          marginBottom: 30,
          borderRadius: 2,
        }}
      />

      {subtitle && (
        <div
          style={{
            fontSize: 32,
            opacity: Math.max(0, subtitleOpacity),
            transform: `translateY(${subtitleY}px)`,
            textAlign: 'center',
            color: '#94A3B8',
          }}
        >
          {subtitle}
        </div>
      )}
    </AbsoluteFill>
  );
};
