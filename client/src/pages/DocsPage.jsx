import React from 'react'
import styles from '@/styles/DocsPage.module.css'
import { Link } from 'wouter'

function DocsPage() {
  return (
    <div className={styles.base}>
      <div className={styles.title}>
        <h2>Documentación de JOLC</h2>
      </div>
      <h3>Manuales</h3>
      <ul>
        <li>
          <Link to='./'>Manual de usuario</Link>
        </li>
        <li>
          <Link to='./'>Manual técnico</Link>
        </li>
      </ul>
      <h3>Contacto</h3>
      <ul>
        <li>
          <Link to='./'>Correo: pablofernando50259107@gmail.com</Link>
        </li>
        <li>
          <Link to='./'>Perfil de Linkedin</Link>
        </li>
      </ul>
    </div>
  )
}

export default DocsPage
