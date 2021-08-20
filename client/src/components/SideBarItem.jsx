import React from 'react'
import styles from '@/styles/SideBarItem.module.css'
import { toggleSideBar } from '@/actions/sideBarActions'
import { Link } from 'wouter'
import { useDispatch } from 'react-redux'

function SideBarItem({ to, active, label }) {
  const dispatch = useDispatch()
  const handleClick = () => {
    dispatch(toggleSideBar())
  }
  return (
    <div className={styles.base} style={active ? { background: 'rgb(40,40,50)' } : {}}>
      <Link to={to} onClick={handleClick}>
        {(active ? '> ' : '') + label}
      </Link>
    </div>
  )
}

export default SideBarItem
