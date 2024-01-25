import { changeSelectedTab } from '@/actions/appActions'
import styles from '@/styles/ReportsArea.module.css'
import { graphviz } from 'd3-graphviz'
import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import ArrowIcon from '/assets/arrow.svg?react'

function ReportsArea({ open }) {
  const dispatch = useDispatch()
  const { ast, symbols, errors, optimizations } = useSelector(
    (state) => state.reports
  )
  const [expanded, setExpanded] = useState(false)

  useEffect(() => {
    setExpanded(false)
  }, [open])

  const { variables, functions, structs } = Boolean(symbols) && symbols

  const existsVariables = Boolean(variables) && Boolean(variables.length)
  const existsFunctions = Boolean(functions) && Boolean(functions.length)
  const existsStructs = Boolean(structs) && Boolean(structs.length)

  const existsAST = Boolean(ast)
  const existsSymbols = existsVariables || existsFunctions || existsStructs
  const existsErrors = Boolean(errors) && Boolean(errors.length)
  const existsOptimizations =
    Boolean(optimizations) && Boolean(optimizations.length)
  const existsReports =
    existsAST || existsSymbols || existsErrors || existsOptimizations

  useEffect(() => {
    const element = document.querySelector(`.${styles.graph}`)

    if (!element || !existsAST) return
    graphviz(element, { useWorker: false, fade: true })
      .attributer((dot) => {
        if (dot.tag == 'polygon') {
          dot.attributes.fill = 'transparent'
          if (dot.key !== 'path-0') dot.attributes.stroke = '#77a9fd'
        }
        if (dot.tag == 'ellipse') {
          dot.attributes.stroke = 'white'
        }
        if (dot.tag == 'text') {
          dot.attributes.fill = 'white'
        }
        if (dot.tag == 'path') {
          dot.attributes.stroke = '#77a9fd'
        }
      })
      .renderDot(ast)
  }, [styles.graph, ast])

  return (
    <div
      className={`${styles.base} ${open ? styles.open : ''} ${
        expanded ? styles.expanded : ''
      }`}
    >
      <div className={styles.content}>
        <button
          title="Expandir reportes"
          className={styles.expand}
          onClick={() => setExpanded(true)}
        >
          <ArrowIcon />
        </button>
        <div className={styles.reports}>
          {existsReports ? (
            <>
              <p>Datos sobre la última ejecución de código:</p>
              {existsAST && (
                <div>
                  <h3>AST</h3>
                  <div className={styles.graph} />
                </div>
              )}
              {existsErrors && (
                <>
                  <h3>Reporte de errores</h3>
                  <div className={styles.report}>
                    <Table
                      headers={[
                        'Hora',
                        'Línea',
                        'Columna',
                        'Tipo',
                        'Descripción'
                      ]}
                      body={errors}
                      className={styles.errors}
                    />
                  </div>
                </>
              )}
              {existsOptimizations && (
                <>
                  <h3>Reporte de Optimizaciones</h3>
                  <div className={styles.report}>
                    <Table
                      headers={[
                        'Línea',
                        'Tipo',
                        'Regla',
                        'Expresión original',
                        'Expresión optimizada'
                      ]}
                      body={optimizations}
                      className={styles.optimizations}
                    />
                  </div>
                </>
              )}
              {existsSymbols && (
                <>
                  <h3>Reporte de símbolos</h3>
                  <div className={styles.report}>
                    {existsVariables && (
                      <>
                        <h4>Variables</h4>
                        <Table
                          headers={[
                            'Entorno',
                            'Línea',
                            'Columna',
                            'ID',
                            'Tipo'
                          ]}
                          body={variables}
                          className={styles.variables}
                        />
                      </>
                    )}
                  </div>
                  <div className={styles.report}>
                    {existsFunctions && (
                      <>
                        <h4>Funciones</h4>
                        <Table
                          headers={[
                            'Entorno',
                            'Línea',
                            'Columna',
                            'ID',
                            'Parámetros'
                          ]}
                          body={functions}
                          className={styles.functions}
                        />
                      </>
                    )}
                  </div>
                  <div className={styles.report}>
                    {existsStructs && (
                      <>
                        <h4>Structs</h4>
                        <Table
                          headers={[
                            'Entorno',
                            'Línea',
                            'Columna',
                            'ID',
                            'Atributos'
                          ]}
                          body={structs}
                          className={styles.structs}
                        />
                      </>
                    )}
                  </div>
                </>
              )}
            </>
          ) : (
            <p>
              No existen reportes para mostrar. Ver al{' '}
              <button onClick={() => dispatch(changeSelectedTab('editor'))}>
                editor
              </button>{' '}
              y ejecuta código.
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

function Table({ headers, body, ...props }) {
  return (
    <div>
      <table {...props}>
        <thead>
          <tr>
            {headers.map((col, i) => (
              <th key={i}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {body.map((row, i) => (
            <tr key={i}>
              {row.map((col, j) => (
                <td key={j}>{col}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default ReportsArea
