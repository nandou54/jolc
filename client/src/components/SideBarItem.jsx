import styles from '@/styles/SideBarItem.module.css'
import React from 'react'
import { useDispatch } from 'react-redux'
import { Link } from 'wouter'

import { toggleSideBar } from '@/actions/appActions'

function SideBarItem({ to, label, img, active }) {
  const dispatch = useDispatch()

  const handleClick = () => {
    dispatch(toggleSideBar(false))
  }

  return (
    <Link
      to={to}
      onClick={handleClick}
      className={styles.base}
      style={active ? { background: 'rgb(40, 40, 65)' } : {}}>
      <img src={`https://img.icons8.com/${active ? '64D264' : 'FFFFFF'}/${img}`} />
      {label}
    </Link>
  )
}

export default SideBarItem
