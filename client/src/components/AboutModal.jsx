import { toggleAboutModal } from '@/actions/appActions'
import styles from '@/styles/AboutModal.module.css'
import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

function AboutModal() {
  const dispatch = useDispatch()
  const { showAboutModal } = useSelector(({ app }) => app)

  return (
    <div
      className={`${styles.base} ${showAboutModal ? styles.show : ''}`}
      onClick={() => {
        dispatch(toggleAboutModal(false))
      }}>
      <div className={styles.modal} onClick={(ev) => ev.stopPropagation()}>
        <div className={styles.group}>
          <h2>Más información</h2>
        </div>
        <div className={styles.content}>
          <div className={styles.group}>
            <h3>¿Qué es JOLC?</h3>
            <ul>
              <li>
                Un intérprete de JOLC, una lenguaje de programación basado en Julia ejecutable en la
                web.
              </li>
              <li>
                Un compilador de JOLC, que genera código intermedio de Go totalmente funcional.
              </li>
              <li>
                Un optimizador de código intermedio de Go, a través de optimizaciones locales y
                globales.
              </li>
            </ul>
          </div>
          <div className={styles.group}>
            <h3>Autor</h3>
            <ul>
              <li>
                <a target="blank" href="https://github.com/nandou54">
                  Pablo Pineda
                </a>
              </li>
              <li>
                <a target="blank" href="mailto:nandou54@outlook.com">
                  nandou54@outlook.com
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
                  href="https://www.tutorialspoint.com/julia/julia_basic_syntax.htm">
                  Julia Programming - Basic Syntax
                </a>
              </li>
            </ul>
          </div>
          <div>
            <p>
              Source del proyecto: <a href="https://github.com/nandou54/jolc">GitHub</a>
            </p>
          </div>
          <div>
            <p>
              Iconos proporcionados por <a href="https://www.svgrepo.com/">SVG Repo</a>. Créditos a
              sus respectivos autores.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AboutModal
