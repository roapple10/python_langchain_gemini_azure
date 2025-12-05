import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    target: 'es2020',
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: undefined,
      },
    },
    // Bundle size target: <200KB gzipped
    chunkSizeWarningLimit: 200,
  },
  server: {
    port: 3000,
    open: true,
  },
})

