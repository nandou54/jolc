import React from 'react'
import styles from '@/styles/Logo.module.css'
import { Link } from 'wouter'
import { useDispatch, useSelector } from 'react-redux'
import { toggleSideBar } from '../actions/appActions'

function Logo() {
  const { show } = useSelector((state) => state.app)
  const dispatch = useDispatch()
  const handleClick = () => {
    dispatch(toggleSideBar(false))
  }

  return (
    <Link
      to='.'
      style={{ opacity: show ? '100%' : '0%' }}
      className={styles.base}
      onClick={handleClick}>
      <img src='https://img.icons8.com/color-glass/48/000000/code.png' />
      Jolc
    </Link>
  )
}

export default Logo
