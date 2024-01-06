import axios from 'axios'
import { useDispatch, useSelector } from 'react-redux'

import { toggleLoading, toggleSideBar } from '@/actions/appActions'
import { appendOutput, clearOutput, logOutput } from '@/actions/outputActions'
import { updateReports } from '@/actions/reportsActions'
import useKeyPress from '@/hooks/useKeyPress'
import { API_URL } from '@/constants'

import menuIcon from '/assets/menu.svg?react'
import playIcon from '/assets/play.svg?react'
import compileIcon from '/assets/compile.svg?react'
import blocksOptimizeIcon from '/assets/blocks-optimize.svg?react'
import eyeholeOptimizeIcon from '/assets/eyehole-optimize.svg?react'

function useSideBar() {
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
  useKeyPress('r', handleRun, { alt: true })
  useKeyPress('c', handleCompile, { alt: true })
  useKeyPress('m', handleOptimizeByEyeHole, {
    alt: true
  })
  useKeyPress('b', handleOptimizeByBlocks, {
    alt: true
  })

  const buttons = [
    {
      onClick: handleToggleSideBar,
      label: 'Abrir menú',
      icon: menuIcon,
      shortcut: '[esc]'
    },
    {
      onClick: handleRun,
      label: 'Ejecutar código',
      icon: playIcon,
      shortcut: '[alt]+[r]',
      highlight: true
    },
    {
      onClick: handleCompile,
      label: 'Compilar código',
      icon: compileIcon,
      shortcut: '[alt]+[c]'
    },
    {
      onClick: handleOptimizeByEyeHole,
      label: 'Optimizar por mirilla',
      icon: eyeholeOptimizeIcon,
      shortcut: '[alt]+[m]'
    },
    {
      onClick: handleOptimizeByBlocks,
      label: 'Optimizar por bloques',
      icon: blocksOptimizeIcon,
      shortcut: '[alt]+[b]'
    }
  ]

  return { show, loading, buttons, handleHideSideBar }
}

export default useSideBar
