import React from 'react'
import styles from '@/styles/App.module.css'
import SideBar from './SideBar'
import { Route } from 'wouter'

import WelcomePage from '@/pages/WelcomePage'
import EditorPage from '@/pages/EditorPage'
import ReportsPage from '@/pages/ReportsPage'
import DocsPage from '@/pages/DocsPage'

function App() {
  return (
    <>
      <SideBar />
      <div className={styles.base}>
        <Route path='/'>
          <WelcomePage />
        </Route>
        <Route path='/editor'>
          <EditorPage />
        </Route>
        <Route path='/reports'>
          <ReportsPage />
        </Route>
        <Route path='/docs'>
          <DocsPage />
        </Route>
      </div>
    </>
  )
}

export default App
