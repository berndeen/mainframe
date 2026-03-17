import { ProductAdProps } from '../compositions/product-ad/schema';

export const sampleProducts: ProductAdProps[] = [
  {
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
  },
  {
    title: 'Smart Fitness Band',
    subtitle: 'Track every move. Crush every goal.',
    features: [
      { icon: '❤️', label: 'Heart Rate Monitor' },
      { icon: '🏃', label: 'GPS Tracking' },
      { icon: '💧', label: 'Waterproof IP68' },
    ],
    bgColor: '#1A1A2E',
    accentColor: '#10B981',
    ctaText: 'Get Yours',
    ctaUrl: 'https://example.com/fitness-band',
  },
  {
    title: 'Ultra Slim Laptop',
    subtitle: 'Power meets portability.',
    features: [
      { icon: '💻', label: '14" Retina Display' },
      { icon: '⚡', label: 'M4 Processor' },
      { icon: '🪶', label: 'Under 1kg' },
      { icon: '🔒', label: 'Face ID Unlock' },
    ],
    bgColor: '#0C0C1D',
    accentColor: '#F59E0B',
    ctaText: 'Pre-Order',
    ctaUrl: 'https://example.com/laptop',
  },
];
