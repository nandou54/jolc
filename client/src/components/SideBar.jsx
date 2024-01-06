import styles from '@/styles/SideBar.module.css'
import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import Logo from '@/components/Logo'
import SideBarButton from '@/components/SideBarButton'

import useSideBar from '@/hooks/useSideBar'
import { toggleAboutModal } from '@/actions/appActions'

function SideBar() {
  const dispatch = useDispatch()
  const { buttons, handleHideSideBar } = useSideBar()
  const { show, loading } = useSelector(({ app }) => app)

  const handleInfoButtonClick = () => {
    handleHideSideBar()
    dispatch(toggleAboutModal(true))
  }

  return (
    <div
      className={`${styles.base} ${show ? styles.show : ''} ${
        loading ? styles.loading : ''
      }`}
    >
      <nav className={styles.sidebar}>
        <div className={styles.buttons}>
          <Logo />
          {buttons.map(
            ({ condition = true, ...button }, i) =>
              condition && <SideBarButton key={i} {...button} />
          )}
        </div>
        <button className={styles.info} onClick={handleInfoButtonClick}>
          Más información
        </button>
      </nav>
      <div className={styles.loader}>
        <div className={styles.bar} />
      </div>
      <div className={styles.outside} onClick={handleHideSideBar} />
    </div>
  )
}

export default SideBar
