import '@/styles/index.css'
import React from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux'

import App from '@/components/App'
import store from '@/store'

const mainElement = document.querySelector('main')
const root = createRoot(mainElement)

root.render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>
)
