import React from 'react'
import styles from '@/styles/SideBarButton.module.css'
import { useDispatch, useSelector } from 'react-redux'
import { toggleSideBar } from '@/actions/sideBarActions'

function SideBarButton() {
  const { show } = useSelector((state) => state.sideBar)
  const dispatch = useDispatch()

  const handleToggle = () => {
    dispatch(toggleSideBar())
  }

  return (
    <div className={styles.base} onClick={handleToggle}>
      {show ? '<' : '>'}
    </div>
  )
}

export default SideBarButton
