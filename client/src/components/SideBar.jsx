import React from 'react'
import styles from '@/styles/SideBar.module.css'
import Logo from './Logo'
import SideBarItem from './SideBarItem'
import { useDispatch, useSelector } from 'react-redux'
import { toggleSideBar, navigateSideBar } from '@/actions/sideBarActions'
import SideBarButton from './SideBarButton'

function SideBar() {
  const { show, activePage } = useSelector((state) => state.sideBar)
  const dispatch = useDispatch()

  const handleHide = () => {
    dispatch(toggleSideBar())
  }

  const handleNavigate = (to) => {
    dispatch(navigateSideBar(to))
  }

  const pages = {
    editor: { img: '', label: 'Editor' },
    reports: { img: '', label: 'Reportes' },
    docs: { img: '', label: 'Documentación' }
  }

  return (
    <div className={styles.base}>
      <div className={styles.sidebar} style={{ marginLeft: show ? 0 : -200 }}>
        <div className={styles.logoArea}>
          <Logo />
          <SideBarButton />
        </div>
        {Object.entries(pages).map(([page, { label }]) => (
          <SideBarItem key={page} to={`./${page}`} onClick={() => handleNavigate(page)}>
            {page == activePage ? '> ' + label : label}
          </SideBarItem>
        ))}
      </div>
      <div
        className={styles.outside}
        onClick={handleHide}
        style={{ display: show ? 'block' : 'none' }}
      />
    </div>
  )
}

export default SideBar
