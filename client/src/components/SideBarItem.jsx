import React from 'react'
import styles from '@/styles/SideBarItem.module.css'
import { Link } from 'wouter'

function SideBarItem({ to, onClick, children }) {
  return (
    <div className={styles.base}>
      <Link onClick={onClick} to={to}>
        {children}
      </Link>
    </div>
  )
}

export default SideBarItem
