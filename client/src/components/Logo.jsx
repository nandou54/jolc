import React from 'react'
import styles from '@/styles/Logo.module.css'
import { Link } from 'wouter'
import { useDispatch } from 'react-redux'
import { hideSideBar } from '../actions/appActions'

function Logo() {
  const dispatch = useDispatch()
  const handleClick = () => {
    dispatch(hideSideBar())
  }
  return (
    <Link className={styles.base} to='/client' onClick={handleClick}>
      JOLC
    </Link>
  )
}

export default Logo
