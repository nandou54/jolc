import styles from '@/styles/AboutModal.module.css'
import React from 'react'

function AboutModal() {
  return (
    <div className={styles.base}>
      <div className={styles.group}>
        <h2>JOLC</h2>
      </div>
      <div className={styles.group}>
        <h3>¿Qué es JOLC?</h3>
        <ul>
          <li>
            Un intérprete de JOLC, una lenguaje de programación basado en Julia
            ejecutable en la web.
          </li>
          <li>
            Un compilador de JOLC, que genera código intermedio de Go totalmente
            funcional.
          </li>
          <li>
            Un optimizador de código intermedio de Go, a través de
            optimizaciones locales y globales.
          </li>
        </ul>
      </div>
      <div className={styles.group}>
        <h3>Autor</h3>
        <ul>
          <li>
            <a target="blank" href="https://github.com/nanndo54">
              Pablo Cabrera
            </a>
          </li>
          <li>
            <a target="blank" href="mailto:pablofernando54@outlook.com">
              pablofernando54@outlook.com
            </a>
          </li>
        </ul>
      </div>
      <div className={styles.group}>
        <h3>Enlaces útiles</h3>
        <ul>
          <li>
            <a target="blank" href="https://julialang.org/">
              The Julia Programming Language
            </a>
          </li>
          <li>
            <a
              target="blank"
              href="https://www.tutorialspoint.com/julia/julia_basic_syntax.htm"
            >
              Julia Programming - Basic Syntax
            </a>
          </li>
        </ul>
      </div>
      <div>
        <p>
          Source del proyecto:{' '}
          <a href="https://github.com/nanndo54/jolc">GitHub</a>
        </p>
      </div>
      <div>
        <p>
          Iconos proporcionados por{' '}
          <a href="https://www.svgrepo.com/">SVG Repo</a>. Créditos a sus
          respectivos autores.
        </p>
      </div>
    </div>
  )
}

export default AboutModal
