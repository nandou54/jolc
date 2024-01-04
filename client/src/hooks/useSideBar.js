import axios from 'axios'
import { useDispatch, useSelector } from 'react-redux'
import { useLocation } from 'wouter'

import { toggleLoading, toggleSideBar } from '@/actions/appActions'
import { appendOutput, clearOutput, logOutput } from '@/actions/outputActions'
import { updateReports } from '@/actions/reportsActions'
import useKeyPress from './useKeyPress'
import { API_URL } from '@/constants'

import homeIcon from '/assets/home.svg?react'
import editorIcon from '/assets/editor.svg?react'
import reportsIcon from '/assets/reports.svg?react'

import menuIcon from '/assets/menu.svg?react'
import playIcon from '/assets/play.svg?react'
import compileIcon from '/assets/compile.svg?react'
import blocksOptimizeIcon from '/assets/blocks-optimize.svg?react'
import peepholeOptimizeIcon from '/assets/peephole-optimize.svg?react'

function useSideBar() {
  const [location] = useLocation()
  const { show, loading } = useSelector(({ app }) => app)
  const content = useSelector(({ editor }) => editor)
  const { c3d } = useSelector(({ reports }) => reports)
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
      .post(`${API_URL}/interpret`, { content })
      .then(({ data }) => {
        const duration = performance.now() - start
        setTimeout(
          () => {
            dispatch(appendOutput(data.output))
            const reports = {
              ast: data.ast,
              errors: data.errors,
              symbols: data.symbols
            }
            dispatch(updateReports(reports))

            if (data.errors.length) {
              dispatch(logOutput('Se encontraron errores'))
              const errorsOutput = data.errors.map(
                ([, ln, col, type, description]) =>
                  `[${ln},${col}] ${type}: ${description}`
              )
              dispatch(appendOutput(errorsOutput))
            }

            dispatch(logOutput(`Tiempo de ejecución: ${duration} ms`))
            dispatch(toggleLoading(false))
          },
          duration < 900 ? 900 - duration : 0
        )
      })
      .catch((error) => {
        const duration = performance.now() - start
        setTimeout(
          () => {
            console.log(error)
            dispatch(logOutput('Hubo un problema interpretando el código'))
            dispatch(toggleLoading(false))
          },
          duration < 900 ? 900 - duration : 0
        )
      })
  }

  const handleCompile = () => {
    if (loading) return
    dispatch(clearOutput())

    const start = performance.now()
    dispatch(toggleLoading(true))
    dispatch(logOutput('Compilando el código a C3D:'))

    axios
      .post(`${API_URL}/translate`, { content })
      .then(({ data }) => {
        const duration = performance.now() - start
        setTimeout(
          () => {
            dispatch(appendOutput(data.output.split('\n')))
            const reports = {
              errors: data.errors,
              symbols: data.symbols,
              c3d: data.output
            }
            dispatch(updateReports(reports))

            if (data.errors.length) {
              dispatch(logOutput('Se encontraron errores'))
              const errorsOutput = data.errors.map(
                ([, ln, col, type, description]) =>
                  `[${ln},${col}] ${type}: ${description}`
              )
              dispatch(appendOutput(errorsOutput))
            }

            dispatch(logOutput(`Tiempo de ejecución: ${duration} ms`))
            dispatch(toggleLoading(false))
          },
          duration < 900 ? 900 - duration : 0
        )
      })
      .catch((error) => {
        const duration = performance.now() - start
        setTimeout(
          () => {
            console.log(error)
            dispatch(logOutput('Hubo un problema interpretando el código'))
            dispatch(toggleLoading(false))
          },
          duration < 900 ? 900 - duration : 0
        )
      })
  }

  const handleOptimizeByEyeHole = () => {
    if (loading) return
    if (!c3d) return dispatch(logOutput('No hay código C3D para optimizar'))

    dispatch(clearOutput())

    const start = performance.now()
    dispatch(toggleLoading(true))
    dispatch(logOutput('Optimizando el código C3D por mirilla:'))

    axios
      .post(`${API_URL}/optimize/eyehole`, { content: c3d })
      .then(({ data }) => {
        const duration = performance.now() - start
        setTimeout(
          () => {
            dispatch(appendOutput(data.output.split('\n')))
            const reports = { c3d: data.output, optimizations: data.reports }
            dispatch(updateReports(reports))

            dispatch(logOutput(`Tiempo de ejecución: ${duration} ms`))
            dispatch(toggleLoading(false))
          },
          duration < 900 ? 900 - duration : 0
        )
      })
      .catch((error) => {
        const duration = performance.now() - start
        setTimeout(
          () => {
            console.log(error)
            dispatch(logOutput('Hubo un problema optimizando el C3D'))
            dispatch(toggleLoading(false))
          },
          duration < 900 ? 900 - duration : 0
        )
      })
  }

  const handleOptimizeByBlocks = () => {
    if (loading) return
    if (!c3d) return dispatch(logOutput('No hay código C3D para optimizar'))

    dispatch(clearOutput())

    const start = performance.now()
    dispatch(toggleLoading(true))
    dispatch(logOutput('Optimizando el código C3D por bloques:'))

    axios
      .post(`${API_URL}/optimize/blocks`, { content: c3d })
      .then(({ data }) => {
        const duration = performance.now() - start
        setTimeout(
          () => {
            dispatch(appendOutput(data.output.split('\n')))
            const reports = { c3d: data.output, optimizations: data.reports }
            dispatch(updateReports(reports))

            dispatch(logOutput(`Tiempo de ejecución: ${duration} ms`))
            dispatch(toggleLoading(false))
          },
          duration < 900 ? 900 - duration : 0
        )
      })
      .catch((error) => {
        const duration = performance.now() - start
        setTimeout(
          () => {
            console.log(error)
            dispatch(logOutput('Hubo un problema optimizando el C3D'))
            dispatch(toggleLoading(false))
          },
          duration < 900 ? 900 - duration : 0
        )
      })
  }

  useKeyPress('Escape', handleToggleSideBar)
  useKeyPress('r', location == 'editor' && handleRun, { alt: true })
  useKeyPress('c', location == 'editor' && handleCompile, { alt: true })
  useKeyPress('m', location == 'editor' && handleOptimizeByEyeHole, {
    alt: true
  })
  useKeyPress('b', location == 'editor' && handleOptimizeByBlocks, {
    alt: true
  })

  const items = [
    {
      label: 'Inicio',
      to: '/',
      icon: homeIcon,
      active: location == '/'
    },
    {
      label: 'Editor',
      to: '/editor',
      icon: editorIcon,
      active: location == '/editor'
    },
    {
      label: 'Reportes',
      to: '/reports',
      icon: reportsIcon,
      active: location == '/reports'
    }
  ]

  const buttons = [
    {
      onClick: handleToggleSideBar,
      icon: menuIcon,
      tooltip: 'Abrir menú [esc]'
    },
    {
      onClick: handleRun,
      icon: playIcon,
      tooltip: 'Ejecutar código [alt]+[r]',
      highlight: true,
      condition: location == '/editor'
    },
    {
      onClick: handleCompile,
      icon: compileIcon,
      tooltip: 'Compilar código [alt]+[c]',
      condition: location == '/editor'
    },
    {
      onClick: handleOptimizeByEyeHole,
      icon: peepholeOptimizeIcon,
      tooltip: 'Optimizar por mirilla [alt]+[m]',
      condition: location == '/editor'
    },
    {
      onClick: handleOptimizeByBlocks,
      icon: blocksOptimizeIcon,
      tooltip: 'Optimizar por bloques [alt]+[b]',
      condition: location == '/editor'
    }
  ]

  return { show, loading, items, buttons, handleHideSideBar }
}

export default useSideBar
