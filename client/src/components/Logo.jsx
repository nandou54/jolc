import styles from '@/styles/Logo.module.css'
import React from 'react'
import { useSelector } from 'react-redux'

function Logo() {
  const { show } = useSelector(({ app }) => app)

  return (
    <header className={`${styles.base} ${show ? styles.show : ''} unselectable`}>
      <img src='https://img.icons8.com/color-glass/48/000000/code.png' />
      Jolc
    </header>
  )
}

export default Logo
