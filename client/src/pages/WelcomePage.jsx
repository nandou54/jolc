import React from 'react'
import styles from '@/styles/WelcomePage.module.css'

// import logo from '@img/logo_usac.png'

function WelcomePage() {
  return (
    <div className={styles.base}>
      {/* <div className={styles.title}>
        <h2>Universidad de San Carlos de Guatemala</h2>
        <img src={logo} width={80} />
      </div> */}
      <div className={styles.small}>Agosto - Septiembre de 2021</div>
      <div className={styles.group}>
        <h3>¡Bienvenido a Jolc!</h3>
        <p>El primer proyecto del curso de Organización de Lenguajes y Compiladores 2</p>
      </div>
      <div className={styles.group}>
        <h3>¿Qué es Jolc?</h3>
        <p>Un intérprete de Julia ejecutable en la web.</p>
      </div>
      <div className={styles.group}>
        <h3>Autor</h3>
        <h3>Autor</h3>
        <h3>Autor</h3>
        <h3>Autor</h3>
        <h3>Autor</h3>
        <h3>Autor</h3>
        <h3>Autor</h3>
        <h3>Autor</h3>
        <h3>Autor</h3>
        <h3>Autor</h3>
        <h3>Autor</h3>
        <p>Nombre: Pablo Cabrera</p>
        <p>Carné: 201901698</p>
        <li>
          <a target='blank' href='mailto:pablofernando50259107@gmail.com'>
            Correo: pablofernando50259107@gmail.com
          </a>
        </li>
        <li>
          <a target='blank' href='https://www.linkedin.com/in/pablo-cabrera-2a567b209/'>
            Perfil de Linkedin
          </a>
        </li>
        <br />
        <div>
          Proyecto disponible en <a href='https://github.com/pabloc54/jolc'>GitHub</a>
        </div>
        <div>
          Icons by <a href='https://icons8.com'>Icons8</a>
        </div>
      </div>
    </div>
  )
}

export default WelcomePage
