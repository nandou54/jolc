import styles from '@/styles/EditorPage.module.css'
import React from 'react'

import EditorArea from '@/components/EditorArea'
import ConsoleArea from '@/components/ConsoleArea'

function EditorPage() {
  return (
    <div className={styles.base}>
      <EditorArea />
      {/* <ConsoleArea /> */}
    </div>
  )
}

export default EditorPage
