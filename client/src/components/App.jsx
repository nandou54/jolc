import styles from '@/styles/App.module.css'
import React, { lazy, Suspense } from 'react'

import SideBar from './SideBar'
import { Route, Router } from 'wouter'

const WelcomePage = lazy(() => import('@/pages/WelcomePage'))
const EditorPage = lazy(() => import('@/pages/EditorPage'))
const ReportsPage = lazy(() => import('@/pages/ReportsPage'))

function App() {
  return (
    <Router base='/client/'>
      <SideBar />
      <div className={styles.base}>
        <Suspense fallback={<div className='loader'>Un momento...</div>}>
          <Route path=''>
            <WelcomePage />
          </Route>
          <Route path='editor'>
            <EditorPage />
          </Route>
          <Route path='reports'>
            <ReportsPage />
          </Route>
        </Suspense>
      </div>
    </Router>
  )
}

export default App
