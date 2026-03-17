import React from 'react';
import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

interface AnimatedTextProps {
  text: string;
  fontSize?: number;
  fontWeight?: number;
  color?: string;
  delay?: number;
  style?: React.CSSProperties;
}

export const AnimatedText: React.FC<AnimatedTextProps> = ({
  text,
  fontSize = 48,
  fontWeight = 700,
  color = '#FFFFFF',
  delay = 0,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', ...style }}>
      {text.split('').map((char, i) => {
        const charDelay = delay + i * 2;
        const s = spring({
          frame,
          fps,
          delay: charDelay,
          config: { damping: 12, stiffness: 200 },
        });
        const translateY = interpolate(s, [0, 1], [30, 0]);
        const opacity = interpolate(s, [0, 1], [0, 1]);

        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              fontSize,
              fontWeight,
              color,
              transform: `translateY(${translateY}px)`,
              opacity,
              whiteSpace: char === ' ' ? 'pre' : undefined,
            }}
          >
            {char}
          </span>
        );
      })}
    </div>
  );
};
