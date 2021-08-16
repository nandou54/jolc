import React from 'react'
import styles from '@/styles/WelcomePage.module.css'

import logo from '@img/logo_usac.png'
import { Link } from 'wouter'

function WelcomePage() {
  return (
    <div className={styles.base}>
      <div className={styles.title}>
        <div>
          <h2>Universidad de San Carlos de Guatemala</h2>
        </div>
        <div>
          <img src={logo} width={100} />
        </div>
      </div>
      <small>Agosto de 2021</small>
      <h3>¡Bienvenido a JOLC!</h3>
      <p>Primer proyecto del curso de Organización de Lenguajes y Compiladores 2</p>
      <h3>¿Qué es JOLC?</h3>
      <p>saber prro</p>
      <h3>Autoría del proyecto</h3>
      <p>Pablo Fernando Cabrera Pineda</p>
      <p>Carné: 201901698</p>
      <br />
      <p>
        Proyecto disponible en <Link to='./'>GitHub</Link>
      </p>
    </div>
  )
}

export default WelcomePage
