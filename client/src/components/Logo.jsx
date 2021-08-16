import React from 'react'
import styles from '@/styles/Logo.module.css'
import { Link } from 'wouter'
import { useDispatch } from 'react-redux'
import { navigateSideBar } from '@/actions/sideBarActions'

function Logo() {
  const dispatch = useDispatch()

  const handleNavigate = () => {
    dispatch(navigateSideBar('/'))
  }

  return (
    <div className={styles.base}>
      <Link onClick={handleNavigate} to='./'>
        JOLC
      </Link>
    </div>
  )
}

export default Logo
