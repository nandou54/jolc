import React from 'react'
import styles from '@/styles/SideBarItem.module.css'
import { hideSideBar } from '../actions/appActions'
import { Link } from 'wouter'
import { useDispatch } from 'react-redux'

function SideBarItem({ to, active, label }) {
  const dispatch = useDispatch()
  const handleClick = () => {
    dispatch(hideSideBar())
  }
  return (
    <Link
      to={to}
      onClick={handleClick}
      className={styles.base}
      style={active ? { background: 'rgba(55,55,70,0.5)' } : {}}>
      {(active ? '> ' : '') + label}
    </Link>
  )
}

export default SideBarItem
