import { defineConfig } from 'vite';

export default defineConfig({
  root: './dist/',
  build: {
    outDir: './app-dist',
    minify: false,
    emptyOutDir: true,
  },
});
