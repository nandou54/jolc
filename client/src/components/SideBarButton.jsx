import React from 'react'
import styles from '@/styles/SideBarButton.module.css'

function SideBarButton({ label, onClick, highlight = false }) {
  return (
    <button
      className={styles.base}
      onClick={onClick}
      style={
        highlight
          ? {
              color: 'white',
              background: 'rgb(110, 210, 110)',
              borderColor: 'rgb(100, 150, 100)',
              borserStyle: 'outset'
            }
          : {}
      }>
      {label}
    </button>
  )
}

export default SideBarButton
