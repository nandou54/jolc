import React from 'react'
import styles from '@/styles/ReportsPage.module.css'
import { useSelector } from 'react-redux'
import { Link } from 'wouter'

function ReportsPage() {
  const reports = useSelector((state) => state.reports)
  const { ast, errors, symbols } = reports

  const existsReports = ast.length || errors.length || symbols.length

  const buttons = [
    {
      label: 'AST',
      background: 'linear-gradient(45deg, rgb(50, 50, 120), rgb(160, 50, 150))',
      onClick: () => {}
    },
    {
      label: 'Errores',
      background: 'linear-gradient(45deg, rgb(214, 64, 64), rgb(192, 183, 50))',
      onClick: () => {}
    },
    {
      label: 'Simbolos',
      background: 'linear-gradient(45deg, rgb(106, 214, 64), rgb(50, 147, 192))',
      onClick: () => {}
    }
  ]

  return (
    <div className={styles.base}>
      <h2>Reportes de la aplicación</h2>
      <p>JOLC ofrece una serie de reportes</p>
      <div className={styles.reports}>
        {!existsReports ? (
          <p>
            No existen reportes para mostrar. Ve a <Link to='/editor'>Editor</Link> para
            generar reportes.
          </p>
        ) : (
          buttons.map((button, i) => <ReportButton key={i} {...button} />)
        )}
      </div>
    </div>
  )
}

function ReportButton({ label, background, onClick }) {
  return (
    <div className='unselectable' style={{ background }} onClick={onClick}>
      {label}
    </div>
  )
}

export default ReportsPage
