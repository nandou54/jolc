import axios from 'axios'
import { useDispatch, useSelector } from 'react-redux'
import { useLocation } from 'wouter'

import { toggleLoading, toggleSideBar } from '@/actions/appActions'
import { appendOutput, clearOutput, logOutput } from '@/actions/outputActions'
import { updateReports } from '@/actions/reportsActions'
import useKeyPress from './useKeyPress'

function useSideBar() {
  const [location] = useLocation()
  const { show, loading } = useSelector(({ app }) => app)
  const content = useSelector(({ editor }) => editor)
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
      .post('/api/interpret', { content })
      .then(({ data }) => {
        const duration = performance.now() - start
        setTimeout(
          () => {
            dispatch(appendOutput(data.output))
            const reports = { ast: data.ast, errors: data.errors, symbols: data.symbols }
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

  useKeyPress('Escape', handleToggleSideBar)
  useKeyPress('Enter', handleRun, { ctrl: true })

  const items = [
    {
      label: 'Inicio',
      to: '.',
      img: 'ios-glyphs/30/home.png',
      active: location == '/'
    },
    {
      label: 'Editor',
      to: 'editor',
      img: 'ios-filled/50/web.png',
      active: location == 'editor'
    },
    {
      label: 'Reportes',
      to: 'reports',
      img: 'pastel-glyph/64/report-file--v4.png',
      active: location == 'reports'
    }
  ]

  const buttons = [
    {
      onClick: handleToggleSideBar,
      img: 'ios-filled/50/FFFFFF/menu-rounded.png',
      tooltip: 'Abrir menú [esc]'
    },
    {
      onClick: handleRun,
      img: 'ios-filled/24/FFFFFF/play--v1.png',
      tooltip: 'Ejecutar código [ctrl]+[enter]',
      highlight: true,
      condition: location == 'editor'
    },
    {
      img: 'material-outlined/24/FFFFFF/play-property.png',
      tooltip: 'Compilar código',
      condition: location == 'editor'
    },
    {
      img: 'external-those-icons-fill-those-icons/24/FFFFFF/external-strainer-kitchen-those-icons-fill-those-icons.png',
      tooltip: 'Optimizar por mirilla',
      condition: location == 'editor'
    },
    {
      img: 'ios-glyphs/24/FFFFFF/prototype.png',
      tooltip: 'Optimizar por bloques',
      condition: location == 'editor'
    }
  ]

  return { show, loading, items, buttons, handleHideSideBar }
}

export default useSideBar
