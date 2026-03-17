import React from 'react';
import { AbsoluteFill, Series } from 'remotion';
import { ProductAdProps } from './schema';
import { Intro } from './scenes/Intro';
import { Features } from './scenes/Features';
import { CTA } from './scenes/CTA';
import { poppinsFont } from '../../lib/fonts';

export const ProductAd: React.FC<ProductAdProps> = (props) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: props.bgColor,
        fontFamily: poppinsFont,
        color: '#F8FAFC',
      }}
    >
      <Series>
        <Series.Sequence durationInFrames={90}>
          <Intro title={props.title} subtitle={props.subtitle} accentColor={props.accentColor} />
        </Series.Sequence>
        <Series.Sequence durationInFrames={120}>
          <Features features={props.features} accentColor={props.accentColor} />
        </Series.Sequence>
        <Series.Sequence durationInFrames={90}>
          <CTA ctaText={props.ctaText} accentColor={props.accentColor} />
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};
