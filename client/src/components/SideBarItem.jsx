import React from 'react'
import styles from '@/styles/SideBarItem.module.css'
import { toggleSideBar } from '../actions/appActions'
import { Link } from 'wouter'
import { useDispatch } from 'react-redux'

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
      <img src={`https://img.icons8.com/${active ? '77CC77' : 'FFFFFF'}/${img}`} />
      {label}
    </Link>
  )
}

export default SideBarItem
