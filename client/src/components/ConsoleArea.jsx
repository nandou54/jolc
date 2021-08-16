import React from 'react'
import styles from '@/styles/ConsoleArea.module.css'
import { useSelector } from 'react-redux'

function ConsoleArea() {
  const output = useSelector((state) => state.output)

  return (
    <div className={styles.base}>
      <textarea readOnly value={output.map((line) => '> ' + line).join('\n')} />
    </div>
  )
}

export default ConsoleArea
