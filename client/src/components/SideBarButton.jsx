import React from 'react'
import styles from '@/styles/SideBarButton.module.css'

function SideBarButton({ onClick, img, highlight }) {
  return (
    <button
      className={styles.base}
      onClick={onClick}
      style={
        highlight
          ? {
              color: 'white',
              background: 'rgb(100, 190, 100)'
            }
          : {}
      }>
      <img src={`https://img.icons8.com/${img}`} />
    </button>
  )
}

export default SideBarButton
