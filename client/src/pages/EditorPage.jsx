import React from 'react'
import Split from 'react-split-grid'
import styles from '@/styles/EditorPage.module.css'

import EditorArea from '@/components/EditorArea'
import ConsoleArea from '@/components/ConsoleArea'

function EditorPage() {
  return (
    <Split
      minSize={300}
      render={({ getGridProps, getGutterProps }) => (
        <div className={styles.base} {...getGridProps()}>
          <EditorArea />
          <div className={styles.gutter} {...getGutterProps('column', 1)} />
          <ConsoleArea />
        </div>
      )}
    />
  )
}

export default EditorPage
