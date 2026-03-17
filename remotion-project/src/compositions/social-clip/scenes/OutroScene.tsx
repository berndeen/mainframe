import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { fadeIn, scaleIn } from '../../../lib/animations';

interface OutroSceneProps {
  handle?: string;
}

export const OutroScene: React.FC<OutroSceneProps> = ({ handle }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = fadeIn(frame, 20);
  const scale = scaleIn(frame, fps);

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          textAlign: 'center',
          transform: `scale(${scale})`,
          opacity,
        }}
      >
        <div style={{ fontSize: 36, fontWeight: 700, marginBottom: 16 }}>
          Follow for more
        </div>
        {handle && (
          <div style={{ fontSize: 28, opacity: 0.8 }}>
            {handle}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
