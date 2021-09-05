import { useLocation } from 'wouter'
import React from 'react'
import axios from 'axios'
import styles from '@/styles/SideBar.module.css'
import useKey from '@/hooks/useKey'
import Logo from './Logo'
import SideBarItem from './SideBarItem'
import SideBarButton from './SideBarButton'
import { toggleLoading, toggleSideBar } from '@/actions/appActions'
import { updateReports } from '@/actions/reportsActions'
import { logOutput, appendOutput, clearOutput } from '@/actions/outputActions'
import { useDispatch, useSelector } from 'react-redux'

function SideBar() {
  const [location] = useLocation()
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
    dispatch(clearOutput())

    const start = performance.now()
    dispatch(toggleLoading(true))
    dispatch(logOutput('Interpretando el código:'))

    axios
      .post('/api/', { content })
      .then(({ data }) => {
        console.log(data)
        dispatch(appendOutput(data.output))
        const reports = { ast: data.ast, errors: data.errors, symbols: data.symbols }
        dispatch(updateReports(reports))

        if (data.errors.length) {
          dispatch(logOutput('Se encontraron errores'))
          const errorsOutput = data.errors.map(
            ({ ln, col, type, description }) => `[${ln},${col}] ${type}: ${description}`
          )
          dispatch(appendOutput(errorsOutput))
        }

        const duration = performance.now() - start
        setTimeout(
          () => {
            dispatch(logOutput(`Tiempo de ejecución: ${duration} ms`))
            dispatch(toggleLoading(false))
          },
          duration < 900 ? 900 - duration : 0
        )
      })
      .catch(() => {
        const duration = performance.now() - start
        setTimeout(
          () => {
            dispatch(logOutput('Hubo un problema interpretando el código'))
            dispatch(toggleLoading(false))
          },
          duration < 900 ? 900 - duration : 0
        )
      })
  }

  useKey('Enter', handleRun, { ctrl: true }, location.includes('editor'))

  const items = [
    {
      to: 'editor',
      label: 'Editor',
      img: 'pastel-glyph/64/seo-text--v1.png',
      active: location.includes('editor')
    },
    {
      to: 'reports',
      label: 'Reportes',
      img: 'pastel-glyph/64/report-file--v4.png',
      active: location.includes('reports')
    }
  ]

  const buttons = [
    {
      onClick: handleToggleSideBar,
      img: 'ios-filled/50/FFFFFF/menu-2.png'
    },
    {
      onClick: handleRun,
      img: 'material-outlined/24/FFFFFF/play--v1.png',
      highlight: true,
      condition: location.includes('editor')
    }
  ]

  return (
    <div className={styles.base}>
      <div className={styles.sidebar} style={{ marginLeft: show ? 0 : -193 }}>
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
      {show && (
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

export default SideBar
