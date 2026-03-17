import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { scaleIn, fadeIn } from '../../../lib/animations';

interface HeadlineSceneProps {
  headline: string;
}

export const HeadlineScene: React.FC<HeadlineSceneProps> = ({ headline }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = scaleIn(frame, fps);
  const opacity = fadeIn(frame, 15);

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
          fontSize: 64,
          fontWeight: 800,
          textAlign: 'center',
          transform: `scale(${scale})`,
          opacity,
          textShadow: '0 4px 20px rgba(0,0,0,0.3)',
        }}
      >
        {headline}
      </div>
    </AbsoluteFill>
  );
};
