import React from 'react'
import styles from '@/styles/SideBar.module.css'
import Logo from './Logo'
import SideBarItem from './SideBarItem'
import { useDispatch, useSelector } from 'react-redux'
import { toggleSideBar } from '@/actions/sideBarActions'
import { newOutput } from '@/actions/outputActions'
import SideBarButton from './SideBarButton'
import { useLocation } from 'wouter'

const pages = [
  { to: 'editor', img: '', label: 'Editor' },
  { to: 'reports', img: '', label: 'Reportes' }
  //{to:docs, img: '', label: 'Documentación' }
]

function SideBar() {
  const [activePage] = useLocation()
  const { show } = useSelector((state) => state.sideBar)
  const dispatch = useDispatch()

  const handleToggle = () => {
    dispatch(toggleSideBar())
  }

  const handleRun = () => {
    dispatch(newOutput('quepex'))
  }

  return (
    <div className={styles.base}>
      <div className={styles.sidebar} style={{ marginLeft: show ? 0 : -200 }}>
        <div className={styles.pages}>
          <Logo />
          {pages.map(({ to, label }) => (
            <SideBarItem
              key={to}
              to={`/client/${to}`}
              label={label}
              active={activePage.includes(to)}
            />
          ))}
        </div>
        <div className={styles.buttons}>
          <SideBarButton label={show ? '<' : '>'} onClick={handleToggle} />
          <SideBarButton label={'R'} onClick={handleRun} highlight />
        </div>
      </div>
      <div
        className={styles.outside}
        onClick={handleToggle}
        style={{ display: show ? 'block' : 'none' }}
      />
    </div>
  )
}

export default SideBar
