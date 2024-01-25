import styles from '@/styles/App.module.css'
import { useDispatch, useSelector } from 'react-redux'

import { changeSelectedTab } from '@/actions/appActions'
import AboutModal from '@/components/AboutModal'
import SideBar from '@/components/SideBar'

import ConsoleArea from '@/components/ConsoleArea'
import EditorArea from '@/components/EditorArea'

import ReportsArea from '@/components/ReportsArea'
import consoleIcon from '/assets/console.svg?react'
import editorIcon from '/assets/editor.svg?react'
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
  const { selectedTab } = useSelector(({ app }) => app)

  return (
    <div className={styles.base}>
      <SideBar />
      <div className={styles.content}>
        <div className={styles.component}>
          {tabs.map((tab) => (
            <tab.component key={tab.id} open={selectedTab === tab.id} />
          ))}
        </div>
        <div className={styles.tabs}>
          {tabs.map((tab) => (
            <button
              key={tab.name}
              className={`${styles.tab} ${
                tab.id === selectedTab ? styles.current : ''
              }`}
              onClick={() =>
                dispatch(
                  changeSelectedTab(tab.id === selectedTab ? 'editor' : tab.id)
                )
              }
            >
              <span>{tab.name}</span>
              <tab.icon />
            </button>
          ))}
        </div>
      </div>
      <AboutModal />
    </div>
  )
}

export default App
