import styles from '@/styles/SideBar.module.css'
import React from 'react'

import Logo from './Logo'
import SideBarButton from './SideBarButton'

import useSideBar from '@/hooks/useSideBar'

function SideBar() {
  const { show, loading, buttons, handleHideSideBar } = useSideBar()

  return (
    <div className={styles.base}>
      <nav className={`${styles.sidebar} ${show ? styles.show : ''}`}>
        <div>
          <Logo />
          <div className={styles.buttons}>
            {buttons.map(
              ({ condition = true, ...button }, i) =>
                condition && <SideBarButton key={i} {...button} />
            )}
          </div>
        </div>
      </nav>
      {loading && <Loader />}
      {(show || loading) && (
        <div
          className={styles.outside}
          onClick={() => handleHideSideBar(false)}
        />
      )}
    </div>
  )
}

function Loader() {
  return (
    <div className={styles.loader}>
      <div className={styles.bar} />
    </div>
  )
}

export default SideBar
