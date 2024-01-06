import styles from '@/styles/App.module.css'
import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import AboutModal from '@/components/AboutModal'
import SideBar from '@/components/SideBar'
import { changeSelectedTab } from '@/actions/appActions'

import EditorArea from '@/components/EditorArea'
import ConsoleArea from '@/components/ConsoleArea'
import ReportsArea from '@/components/ReportsArea'

import editorIcon from '/assets/editor.svg?react'
import consoleIcon from '/assets/console.svg?react'
import reportsIcon from '/assets/reports.svg?react'

const tabs = [
  {
    id: 'editor',
    name: 'Editor',
    icon: editorIcon,
    component: EditorArea
  },
  {
    id: 'console',
    name: 'Consola',
    icon: consoleIcon,
    component: ConsoleArea
  },
  {
    id: 'reports',
    name: 'Reportes',
    icon: reportsIcon,
    component: ReportsArea
  }
]

function App() {
  const dispatch = useDispatch()
  const { selectedTab: selectedTabId } = useSelector(({ app }) => app)

  const selectedTab = tabs.find(({ id }) => id === selectedTabId)

  return (
    <div className={styles.base}>
      <SideBar />
      <div className={styles.content}>
        <div className={styles.tabs}>
          {tabs.map((tab) => (
            <button
              key={tab.name}
              className={`${styles.tab} ${
                tab.id === selectedTabId ? styles.current : ''
              }`}
              onClick={() => dispatch(changeSelectedTab(tab.id))}
            >
              <span>{tab.name}</span>
              <tab.icon />
            </button>
          ))}
        </div>
        <div className={styles.component}>
          <selectedTab.component />
        </div>
      </div>
      <AboutModal />
    </div>
  )
}

export default App
