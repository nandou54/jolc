import React from 'react'
import styles from '@/styles/EditorPage.module.css'

import EditorArea from '@/components/EditorArea'
import ConsoleArea from '@/components/ConsoleArea'
import RunButton from '../components/RunButton'

function EditorPage() {
  return (
    <>
      <div className={styles.base}>
        <EditorArea />
        <ConsoleArea />
      </div>
      <RunButton />
    </>
  )
}

export default EditorPage
