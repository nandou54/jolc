import { changeSelectedTab } from '@/actions/appActions'
import styles from '@/styles/ConsoleArea.module.css'
import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import ArrowIcon from '/assets/arrow.svg?react'

function ConsoleArea({ open }) {
  const dispatch = useDispatch()
  const output = useSelector((state) => state.output)
  const [expanded, setExpanded] = useState(false)

  useEffect(() => {
    setExpanded(false)
  }, [open])

  return (
    <div
      className={`${styles.base} ${open ? styles.open : ''} ${
        expanded ? styles.expanded : ''
      }`}
      onClick={() => dispatch(changeSelectedTab('editor'))}
    >
      <div className={styles.content} onClick={(ev) => ev.stopPropagation()}>
        <button
          title="Expandir consola"
          className={styles.expand}
          onClick={() => setExpanded(true)}
        >
          <ArrowIcon />
        </button>
        <ul className={styles.console}>
          {output.map((line, i) => (
            <li key={i}>{line}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default ConsoleArea
