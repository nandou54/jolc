import React from 'react'
import styles from '@/styles/RunButton.module.css'
import { useDispatch } from 'react-redux'

import { newOutput } from '@/actions/outputActions'

function RunButton() {
  const dispatch = useDispatch()

  const handleRun = () => {
    dispatch(newOutput('quepex'))
  }

  return (
    <div className={styles.base} onClick={handleRun}>
      Run
    </div>
  )
}

export default RunButton
