import React from 'react'
import styles from '@/styles/ReportsPage.module.css'
import { useSelector } from 'react-redux'
import { Link } from 'wouter'

function ReportsPage() {
  const { ast, errors, symbols } = useSelector((state) => state.reports)

  const existsReports = ast.length || errors.length || symbols.length

  const variables = symbols.filter(({ symbolType }) => symbolType == 'variable')
  const functions = symbols.filter(({ symbolType }) => symbolType == 'function')
  const structs = symbols.filter(({ symbolType }) => symbolType == 'struct')

  return (
    <div className={styles.base}>
      <div className={styles.small}>Agosto - Septiembre de 2021</div>
      <h2>Reportes de la aplicación</h2>
      <p>JOLC ofrece una serie de reportes</p>
      {!existsReports ? (
        <p>
          No existen reportes para mostrar. Ve al <Link to='editor'>Editor</Link> para
          generar reportes.
        </p>
      ) : (
        <>
          {/* <div>
            <h2>AST</h2>
            {JSON.stringify(ast)}
          </div> */}
          <h2>Reporte de errores</h2>
          <div className={styles.report}>
            <div>
              <table className={styles.errors}>
                <thead>
                  <th>Hora</th>
                  <th>Línea</th>
                  <th>Columna</th>
                  <th>Tipo</th>
                  <th>Descripción</th>
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
          </div>
          <h2>Reporte de símbolos</h2>
          <div className={styles.report}>
            <h3>Variables</h3>
            <div>
              <table className={styles.variables}>
                <thead>
                  <th>Entorno</th>
                  <th>Línea</th>
                  <th>Columna</th>
                  <th>ID</th>
                  <th>Tipo</th>
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
          </div>
          <div className={styles.report}>
            <h3>Funciones</h3>
            <div>
              <table className={styles.functions}>
                <thead>
                  <th>Entorno</th>
                  <th>Línea</th>
                  <th>Columna</th>
                  <th>ID</th>
                  <th>Parametros</th>
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
          </div>
          <div className={styles.report}>
            <h3>Structs</h3>
            <div>
              <table className={styles.structs}>
                <thead>
                  <th>Entorno</th>
                  <th>Línea</th>
                  <th>Columna</th>
                  <th>ID</th>
                  <th>Atributos</th>
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
          </div>
        </>
      )}
    </div>
  )
}

export default ReportsPage
