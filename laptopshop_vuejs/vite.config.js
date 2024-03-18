import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  server: {				// ← ← ← ← ← ←
    host: '0.0.0.0'	// ← new content ←
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  headers: {
    "Access-Control-Allow-Origin": "*",
  }
})
