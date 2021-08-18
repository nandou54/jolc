import { defineConfig } from 'vite'
import reactRefresh from '@vitejs/plugin-react-refresh'
import path from 'path'

export default defineConfig({
  // base: '/client/',
  // build: {
  //   emptyOutDir: true,
  //   outDir: '../dist'
  // },
  plugins: [reactRefresh()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, '/src'),
      '@img': path.resolve(__dirname, '/img')
    }
  },
  css: {
    modules: {
      generateScopedName: (name, filename, css) => {
        const index = css.indexOf('.' + name)
        const line = css.substr(0, index).split(/[\r\n]/).length

        const file = path.basename(filename).split('.')[0]

        return `${file}_${name}_${line}`
      }
    }
  }
})
