import { z } from 'zod';
import { CalculateMetadataFunction } from 'remotion';

export const socialClipSchema = z.object({
  headline: z.string().min(1).max(80),
  bodyLines: z.array(z.string()).min(1).max(6),
  bgGradientFrom: z.string().regex(/^#[0-9a-fA-F]{6}$/),
  bgGradientTo: z.string().regex(/^#[0-9a-fA-F]{6}$/),
  handle: z.string().max(30).optional(),
});

export type SocialClipProps = z.infer<typeof socialClipSchema>;

export const sampleSocialClipProps: SocialClipProps = {
  headline: 'Did You Know?',
  bodyLines: [
    'React components can become videos.',
    'Every frame is a render.',
    'Code is the timeline.',
  ],
  bgGradientFrom: '#4338CA',
  bgGradientTo: '#EC4899',
  handle: '@yourhandle',
};

export const calculateSocialClipMetadata: CalculateMetadataFunction<SocialClipProps> = async ({
  props,
}) => {
  // 2 seconds per body line + 2s intro + 1.5s outro
  const fps = 30;
  const introFrames = 60;
  const perLineFrames = 60;
  const outroFrames = 45;
  const durationInFrames = introFrames + props.bodyLines.length * perLineFrames + outroFrames;

  return {
    durationInFrames,
    fps,
    width: 1080,
    height: 1080,
  };
};
