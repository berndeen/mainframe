import { z } from 'zod';

export const productAdSchema = z.object({
  title: z.string().min(1).max(60),
  subtitle: z.string().max(100).optional(),
  features: z
    .array(
      z.object({
        icon: z.string(),
        label: z.string().max(40),
      }),
    )
    .min(1)
    .max(5),
  bgColor: z.string().regex(/^#[0-9a-fA-F]{6}$/),
  accentColor: z.string().regex(/^#[0-9a-fA-F]{6}$/),
  ctaText: z.string().max(30),
  ctaUrl: z.string().url(),
  logoUrl: z.string().url().optional(),
  imageUrl: z.string().url().optional(),
});

export type ProductAdProps = z.infer<typeof productAdSchema>;

export const sampleProductAdProps: ProductAdProps = {
  title: 'Next-Gen Headphones',
  subtitle: 'Immersive sound. All day comfort.',
  features: [
    { icon: '🎵', label: 'Hi-Fi Audio' },
    { icon: '🔋', label: '40hr Battery' },
    { icon: '🎤', label: 'Active Noise Cancel' },
    { icon: '📱', label: 'Seamless Pairing' },
  ],
  bgColor: '#0F172A',
  accentColor: '#6366F1',
  ctaText: 'Shop Now',
  ctaUrl: 'https://example.com/headphones',
};
