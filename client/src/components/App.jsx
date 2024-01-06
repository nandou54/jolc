import styles from '@/styles/App.module.css'
import React, { lazy, Suspense } from 'react'

import SideBar from '@/components/SideBar'
import AboutModal from '@/pages/AboutModal'

const EditorPage = lazy(() => import('@/pages/EditorPage'))

function App() {
  return (
    <div className={styles.base}>
      <SideBar />
      <div className={styles.content}>
        <Suspense fallback={<div className="loader">Un momento...</div>}>
          <EditorPage />
          <AboutModal />
        </Suspense>
      </div>
    </div>
  )
}

export default App
