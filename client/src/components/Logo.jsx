import styles from '@/styles/Logo.module.css'
import React from 'react'
import { useSelector } from 'react-redux'

function Logo() {
  const { show } = useSelector(({ app }) => app)

  return (
    <header
      className={`${styles.base} ${show ? styles.show : ''} unselectable`}
    >
      <img src="/favicon.svg" />
      JOLC
    </header>
  )
}

export default Logo
