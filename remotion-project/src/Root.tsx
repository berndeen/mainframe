import React from 'react';
import { Composition } from 'remotion';
import { ProductAd } from './compositions/product-ad/ProductAd';
import { productAdSchema, sampleProductAdProps } from './compositions/product-ad/schema';
import { SocialClip } from './compositions/social-clip/SocialClip';
import {
  socialClipSchema,
  sampleSocialClipProps,
  calculateSocialClipMetadata,
} from './compositions/social-clip/schema';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="ProductAd"
        component={ProductAd}
        schema={productAdSchema}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={sampleProductAdProps}
      />
      <Composition
        id="SocialClip"
        component={SocialClip}
        schema={socialClipSchema}
        calculateMetadata={calculateSocialClipMetadata}
        fps={30}
        width={1080}
        height={1080}
        durationInFrames={150}
        defaultProps={sampleSocialClipProps}
      />
    </>
  );
};
