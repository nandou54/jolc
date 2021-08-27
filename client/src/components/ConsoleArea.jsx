import React from 'react'
import styles from '@/styles/ConsoleArea.module.css'
import { useSelector } from 'react-redux'

function ConsoleArea() {
  const output = useSelector((state) => state.output)

  return (
    <div className={styles.base}>
      <div className={`${styles.title} unselectable`}>console</div>
      <div className={styles.console}>
        <ul>
          {output.map((line, i) => (
            <li key={i}>{line}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default ConsoleArea
