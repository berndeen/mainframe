import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, Sequence } from 'remotion';
import { SocialClipProps } from './schema';
import { HeadlineScene } from './scenes/HeadlineScene';
import { BodyLineScene } from './scenes/BodyLineScene';
import { OutroScene } from './scenes/OutroScene';
import { interFont } from '../../lib/fonts';

export const SocialClip: React.FC<SocialClipProps> = (props) => {
  const { durationInFrames } = useVideoConfig();

  const introFrames = 60;
  const perLineFrames = 60;
  const outroFrames = 45;

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(135deg, ${props.bgGradientFrom}, ${props.bgGradientTo})`,
        fontFamily: interFont,
        color: '#FFFFFF',
      }}
    >
      <Sequence from={0} durationInFrames={introFrames}>
        <HeadlineScene headline={props.headline} />
      </Sequence>

      {props.bodyLines.map((line, i) => (
        <Sequence
          key={i}
          from={introFrames + i * perLineFrames}
          durationInFrames={perLineFrames}
        >
          <BodyLineScene
            line={line}
            index={i}
            total={props.bodyLines.length}
          />
        </Sequence>
      ))}

      <Sequence from={durationInFrames - outroFrames} durationInFrames={outroFrames}>
        <OutroScene handle={props.handle} />
      </Sequence>
    </AbsoluteFill>
  );
};
