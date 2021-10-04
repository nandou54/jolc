import styles from '@/styles/WelcomePage.module.css'
import React from 'react'

import logo from '@img/logo_usac.png'

function WelcomePage() {
  return (
    <div className={styles.base}>
      <div className={styles.small}>Agosto - Septiembre de 2021</div>
      <div className={styles.title}>
        <h2>Universidad de San Carlos de Guatemala</h2>
        <img src={logo} width={100} />
      </div>
      <div className={styles.group}>
        <h3>¡Bienvenido a Jolc!</h3>
        <p>El primer proyecto del curso de Organización de Lenguajes y Compiladores 2</p>
      </div>
      <div className={styles.group}>
        <h3>¿Qué es Jolc?</h3>
        <p>
          Un intérprete de un lenguaje llamado Jolc, una lenguaje basado en Julia
          ejecutable en la web.
        </p>
      </div>
      <div className={styles.group}>
        <h3>Autor</h3>
        <p>Nombre: Pablo Cabrera</p>
        <p>Carné: 201901698</p>
        <li>
          <a target='blank' href='mailto:pablofernando50259107@gmail.com'>
            E-mail
          </a>
        </li>
        <br />
        <div>
          Source del proyecto: <a href='https://github.com/pabloc54/jolc'>GitHub</a>
        </div>
        <div>
          Icons by <a href='https://icons8.com'>Icons8</a>
        </div>
      </div>
    </div>
  )
}

export default WelcomePage
