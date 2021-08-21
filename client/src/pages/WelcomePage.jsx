import React from 'react'
import styles from '@/styles/WelcomePage.module.css'

import logo from '@img/logo_usac.png'

function WelcomePage() {
  return (
    <div className={styles.base}>
      <div className={styles.title}>
        <h2>Universidad de San Carlos de Guatemala</h2>
        <img src={logo} width={80} />
      </div>
      <div className={styles.small}>Agosto de 2021</div>
      <div className={styles.group}>
        <h3>¡Bienvenido a JOLC!</h3>
        <p>
          JOLC es el primer proyecto del curso de Organización de Lenguajes y Compiladores
          2
        </p>
      </div>
      <div className={styles.group}>
        <h3>¿Qué es JOLC?</h3>
        <p>saber prro</p>
      </div>
      <div className={styles.group}>
        <h3>Contacto</h3>
        <div>
          <a target='blank' href='mailto:pablofernando50259107@gmail.com'>
            Correo: pablofernando50259107@gmail.com
          </a>
        </div>
        <div>
          <a target='blank' href='https://www.linkedin.com/in/pablo-cabrera-2a567b209/'>
            Perfil de Linkedin
          </a>
        </div>
        <div>
          Proyecto disponible en{' '}
          <a target='blank' href='https://github.com/pabloc54/jolc'>
            GitHub
          </a>
        </div>
      </div>
    </div>
  )
}

export default WelcomePage
