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
              background: 'rgb(119, 203, 119)'
            }
          : {}
      }>
      <img src={`https://img.icons8.com/${img}`} />
    </button>
  )
}

export default SideBarButton
