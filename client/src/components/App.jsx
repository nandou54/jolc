import styles from '@/styles/App.module.css'
import React, { lazy, Suspense } from 'react'

import SideBar from './SideBar'

const EditorPage = lazy(() => import('@/pages/EditorPage'))

function App() {
  return (
    <div>
      <SideBar />
      <div className={styles.base}>
        <Suspense fallback={<div className="loader">Un momento...</div>}>
          <EditorPage />
        </Suspense>
      </div>
    </div>
  )
}

export default App
