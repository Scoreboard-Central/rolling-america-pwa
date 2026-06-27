import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'rolling_america.myapp',
  appName: 'Rolling America',
  webDir: 'dist/rolling-america-pwa/browser',
  server: {
    androidScheme: 'https'
  }
};

export default config;
