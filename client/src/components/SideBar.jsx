import React from 'react'
import axios from 'axios'
import styles from '@/styles/SideBar.module.css'
import Logo from './Logo'
import SideBarItem from './SideBarItem'
import { useDispatch, useSelector } from 'react-redux'
import { showSideBar, hideSideBar, toggleLoading } from '@/actions/appActions'
import { updateReports } from '@/actions/reportsActions'
import { log, newOutput } from '@/actions/outputActions'
import SideBarButton from './SideBarButton'
import { useLocation } from 'wouter'

const pages = [
  { to: 'editor', img: '', label: 'Editor' },
  { to: 'reports', img: '', label: 'Reportes' },
  { to: 'docs', img: '', label: 'Documentación' }
]

function app() {
  const [activePage] = useLocation()
  const [{ show, loading }, content] = useSelector((state) => [
    state.app,
    state.editorContent
  ])
  const dispatch = useDispatch()

  const handleToggle = () => {
    dispatch(show ? hideSideBar() : showSideBar())
  }

  const handleHide = () => {
    dispatch(hideSideBar())
  }

  const handleRun = () => {
    if (loading) return
    dispatch(toggleLoading())

    axios
      .post('/api', { text: content })
      .then(({ data }) => {
        console.log(data)
        dispatch(updateReports(data))
      })
      .catch((error) => console.log(error))

    dispatch(toggleLoading())
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
        <div className={styles.separator} />
        <div className={styles.buttons}>
          <SideBarButton
            label={
              <img src='https://img.icons8.com/material-outlined/24/000000/menu--v4.png' />
            }
            onClick={handleToggle}
          />
          {activePage.includes('editor') && (
            <SideBarButton label={'run'} onClick={handleRun} highlight />
          )}
        </div>
      </div>
      {loading && <Loader />}
      {(show || loading) && <div className={styles.outside} onClick={handleHide} />}
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
