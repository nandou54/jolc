import styles from '@/styles/SideBarButton.module.css'
import React from 'react'

function SideBarButton({ onClick, img, tooltip = 'none', highlight = false }) {
  return (
    <div className={styles.base}>
      <button
        className={`${styles.button} ${highlight ? styles.highlight : ''}`}
        onClick={onClick}>
        <img src={`https://img.icons8.com/${img}`} />
      </button>
      <div className={styles.tooltip}>{tooltip}</div>
    </div>
  )
}

export default SideBarButton
