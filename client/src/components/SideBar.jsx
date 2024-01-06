import styles from '@/styles/SideBar.module.css'
import React from 'react'
import { useSelector } from 'react-redux'

import Logo from '@/components/Logo'
import SideBarButton from '@/components/SideBarButton'

import useSideBar from '@/hooks/useSideBar'

function SideBar() {
  const { buttons, handleHideSideBar } = useSideBar()
  const { show, loading } = useSelector(({ app }) => app)

  return (
    <div className={`${styles.base} ${show ? styles.show : ''}`}>
      <nav className={styles.sidebar}>
        <Logo className={styles.logo} />
        <div className={styles.buttons}>
          {buttons.map(
            ({ condition = true, ...button }, i) =>
              condition && <SideBarButton key={i} {...button} />
          )}
        </div>
      </nav>
      {loading && (
        <div className={styles.loader}>
          <div className={styles.bar} />
        </div>
      )}
      {(show || loading) && (
        <div
          className={styles.outside}
          onClick={() => handleHideSideBar(false)}
        />
      )}
    </div>
  )
}

export default SideBar
