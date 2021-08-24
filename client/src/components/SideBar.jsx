import React from 'react'
import axios from 'axios'
import styles from '@/styles/SideBar.module.css'
import Logo from './Logo'
import SideBarItem from './SideBarItem'
import { useDispatch, useSelector } from 'react-redux'
import { toggleLoading, toggleSideBar } from '@/actions/appActions'
import { updateReports } from '@/actions/reportsActions'
import { log, newOutput } from '@/actions/outputActions'
import SideBarButton from './SideBarButton'
import { useLocation } from 'wouter'

function app() {
  const [activePage] = useLocation()
  const [{ show, loading }, content] = useSelector((state) => [state.app, state.editor])
  const dispatch = useDispatch()

  const handleToggleSideBar = () => {
    dispatch(toggleSideBar(!show))
  }
  const handleHideSideBar = () => {
    dispatch(toggleSideBar(false))
  }

  const handleRun = () => {
    if (loading) return
    dispatch(toggleLoading(true))

    axios
      .post('/api', { content })
      .then(({ data }) => {
        dispatch(updateReports(data))
        dispatch(newOutput([JSON.stringify(data)]))
        console.log(data)
      })
      .catch((error) => console.log(error))

    dispatch(toggleLoading(false))
  }

  const items = [
    {
      to: '/client/editor',
      label: 'Editor',
      img: 'pastel-glyph/64/seo-text--v1.png',
      active: activePage.includes('editor')
    },
    {
      to: '/client/reports',
      label: 'Reportes',
      img: 'pastel-glyph/64/report-file--v4.png',
      active: activePage.includes('reports')
    }
  ]

  const buttons = [
    {
      onClick: handleToggleSideBar,
      img: 'ios-filled/50/FFFFFF/menu-2.png',
      highlight: false
    },
    {
      onClick: handleRun,
      img: 'material-outlined/24/FFFFFF/play--v1.png',
      highlight: true,
      condition: activePage.includes('editor')
    }
  ]

  return (
    <div className={styles.base}>
      <div className={styles.sidebar} style={{ marginLeft: show ? 0 : -190 }}>
        <Logo />
        <div className={styles.items}>
          {items.map((item, i) => (
            <SideBarItem key={i} {...item} />
          ))}
        </div>
        <div className={styles.separator} />
        <div className={styles.buttons}>
          {buttons.map(
            ({ condition = true, ...button }, i) =>
              condition && <SideBarButton key={i} {...button} />
          )}
        </div>
      </div>
      {loading && <Loader />}
      {(show || loading) && (
        <div className={styles.outside} onClick={() => handleHideSideBar(false)} />
      )}
    </div>
  )
}

function Loader() {
  return (
    <div className={styles.loader}>
      <div className={styles.bar} />
    </div>
  )
}

export default app
