import React from 'react'
import styles from '@/styles/SideBarButton.module.css'

function SideBarButton({ onClick, img, highlight = false }) {
  return (
    <button
      className={styles.base}
      onClick={onClick}
      style={
        highlight
          ? {
              background: 'rgb(100, 210, 100)',
              borderRight: '3px rgb(70, 150, 70) solid'
            }
          : {}
      }>
      <img src={`https://img.icons8.com/${img}`} />
    </button>
  )
}

export default SideBarButton
