import React from 'react'
import styles from '@/styles/ReportsPage.module.css'
import { useSelector } from 'react-redux'
import { Link } from 'wouter'
import { Graphviz } from 'graphviz-react'

function ReportsPage() {
  const { ast, symbols, errors } = useSelector((state) => state.reports)

  const existsAST = !!ast
  const existsErrors = !!errors.length
  const existsSymbols = !!symbols.length
  const existsReports = existsAST || existsErrors || existsSymbols

  const variables = symbols.filter(({ symbolType }) => symbolType == 'variable')
  const functions = symbols.filter(({ symbolType }) => symbolType == 'function')
  const structs = symbols.filter(({ symbolType }) => symbolType == 'struct')

  const existsVariables = !!variables.length
  const existsFunctions = !!functions.length
  const existsStructs = !!structs.length

  return (
    <div className={styles.base}>
      <div className={styles.small}>Agosto - Septiembre de 2021</div>
      <h2>Reportes de la aplicación</h2>
      <p>Datos sobre la última ejecución de código</p>
      {!existsReports ? (
        <p>
          No existen reportes para mostrar. Ve al <Link to='editor'>Editor</Link> para
          generar reportes.
        </p>
      ) : (
        <>
          <div>
            <h3>AST</h3>
            {!existsAST ? (
              <p>Sin datos</p>
            ) : (
              <Graphviz
                className={styles.graph}
                dot={ast}
                options={{
                  width: null,
                  height: null,
                  fit: true
                }}
              />
            )}
          </div>
          <h3>Reporte de errores</h3>
          <div className={styles.report}>
            {!existsErrors ? (
              <p>Sin datos</p>
            ) : (
              <div>
                <table className={styles.errors}>
                  <thead>
                    <tr>
                      <th>Hora</th>
                      <th>Línea</th>
                      <th>Columna</th>
                      <th>Tipo</th>
                      <th>Descripción</th>
                    </tr>
                  </thead>
                  <tbody>
                    {errors.map(({ time, ln, col, type, description }) => (
                      <tr key={time}>
                        <td>{time}</td>
                        <td>{ln}</td>
                        <td>{col}</td>
                        <td>{type}</td>
                        <td>{description}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
          <h3>Reporte de símbolos</h3>
          {!existsSymbols ? (
            <p>Sin datos</p>
          ) : (
            <>
              <div className={styles.report}>
                <h4>Variables</h4>
                {!existsVariables ? (
                  <p>Sin datos</p>
                ) : (
                  <div>
                    <table className={styles.variables}>
                      <thead>
                        <tr>
                          <th>Entorno</th>
                          <th>Línea</th>
                          <th>Columna</th>
                          <th>ID</th>
                          <th>Tipo</th>
                        </tr>
                      </thead>
                      <tbody>
                        {variables.map(({ env, ln, col, id, type }) => (
                          <tr key={col + ',' + id}>
                            <td>{env}</td>
                            <td>{ln}</td>
                            <td>{col}</td>
                            <td>{id}</td>
                            <td>{type}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
              <div className={styles.report}>
                <h4>Funciones</h4>
                {!existsFunctions ? (
                  <p>Sin datos</p>
                ) : (
                  <div>
                    <table className={styles.functions}>
                      <thead>
                        <tr>
                          <th>Entorno</th>
                          <th>Línea</th>
                          <th>Columna</th>
                          <th>ID</th>
                          <th>Parametros</th>
                        </tr>
                      </thead>
                      <tbody>
                        {functions.map(({ env, ln, col, id, parameters }) => (
                          <tr key={col + ',' + id}>
                            <td>{env}</td>
                            <td>{ln}</td>
                            <td>{col}</td>
                            <td>{id}</td>
                            <td>{parameters}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
              <div className={styles.report}>
                <h4>Structs</h4>
                {!existsStructs ? (
                  <p>Sin datos</p>
                ) : (
                  <div>
                    <table className={styles.structs}>
                      <thead>
                        <tr>
                          <th>Entorno</th>
                          <th>Línea</th>
                          <th>Columna</th>
                          <th>ID</th>
                          <th>Atributos</th>
                        </tr>
                      </thead>
                      <tbody>
                        {structs.map(({ env, ln, col, id, attributes }) => (
                          <tr key={col + ',' + id}>
                            <td>{env}</td>
                            <td>{ln}</td>
                            <td>{col}</td>
                            <td>{id}</td>
                            <td>{attributes}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </>
          )}
        </>
      )}
    </div>
  )
}

export default ReportsPage
