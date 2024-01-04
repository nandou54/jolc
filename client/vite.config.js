import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import svgr from 'vite-plugin-svgr'
import path from 'path'

export default defineConfig({
  base: '/jolc/',
  publicDir: 'src/public',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    assetsDir: 'static'
  },
  plugins: [
    react(),
    svgr({
      svgrOptions: {
        plugins: ['@svgr/plugin-svgo', '@svgr/plugin-jsx']
      }
    })
  ],
  resolve: {
    alias: {
      '@': '/src'
    }
  },
  css: {
    modules: {
      generateScopedName: (name, filename, css) => {
        const index = css.indexOf(`.${name}`)
        const line = css.slice(0, index).split(/[\r\n]/).length

        const file = path.basename(filename).split('.')[0]

        return `${file}_${name}_${line}`
      }
    }
  }
})
