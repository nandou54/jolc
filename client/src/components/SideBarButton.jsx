import styles from '@/styles/SideBarButton.module.css'
import React from 'react'
import { useSelector } from 'react-redux'

function SideBarButton({
  onClick,
  label,
  shortcut,
  icon: IconComponent,
  highlight = false
}) {
  const { show } = useSelector(({ app }) => app)

  return (
    <div className={`${styles.base} ${show ? styles.show : ''}`}>
      <button
        className={`${styles.button} ${highlight ? styles.highlight : ''}`}
        onClick={onClick}
      >
        <span className={styles.label}>{label}</span>
        <IconComponent />
      </button>
      <div className={styles.tooltip}>
        {label} {shortcut}
      </div>
    </div>
  )
}

export default SideBarButton
