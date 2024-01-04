import styles from '@/styles/ReportsPage.module.css'
import React from 'react'
import { useSelector } from 'react-redux'
import { Link } from 'wouter'
import { Graphviz } from 'graphviz-react'

function ReportsPage() {
  const { ast, symbols, errors, optimizations } = useSelector(
    (state) => state.reports
  )
  const { variables, functions, structs } = !!symbols && symbols

  const existsVariables = !!variables && !!variables.length
  const existsFunctions = !!functions && !!functions.length
  const existsStructs = !!structs && !!structs.length

  const existsAST = !!ast
  const existsSymbols = existsVariables || existsFunctions || existsStructs
  const existsErrors = !!errors && !!errors.length
  const existsOptimizations = !!optimizations && !!optimizations.length
  const existsReports =
    existsAST || existsSymbols || existsErrors || existsOptimizations

  return (
    <div className={styles.base}>
      <h2>Reportes de la aplicación</h2>
      <p>Datos sobre la última ejecución de código</p>
      {!existsReports ? (
        <p>
          No existen reportes para mostrar. Ve al{' '}
          <Link to="/editor">Editor</Link> para generar reportes.
        </p>
      ) : (
        <>
          {existsAST && (
            <div>
              <h3>AST</h3>
              <Graphviz
                className={styles.graph}
                dot={ast}
                options={{
                  width: null,
                  height: null,
                  fit: true
                }}
              />
            </div>
          )}
          {existsErrors && (
            <>
              <h3>Reporte de errores</h3>
              <div className={styles.report}>
                <Table
                  headers={['Hora', 'Línea', 'Columna', 'Tipo', 'Descripción']}
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
                      headers={['Entorno', 'Línea', 'Columna', 'ID', 'Tipo']}
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
      )}
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

export default ReportsPage
