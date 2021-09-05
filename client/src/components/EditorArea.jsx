import React from 'react'
import styles from '@/styles/EditorArea.module.css'

import { useSelector, useDispatch } from 'react-redux'
import { updateContent } from '@/actions/editorActions'

import AceEditor from 'react-ace'
import 'ace-builds/src-noconflict/mode-julia'
import 'ace-builds/src-noconflict/theme-dracula'

function EditorArea() {
  const content = useSelector((state) => state.editor)
  const dispatch = useDispatch()

  const handleChange = (newContent) => {
    dispatch(updateContent(newContent))
  }

  return (
    <div className={styles.base}>
      <div className={`${styles.title} unselectable`}>editor</div>
      <AceEditor
        className={styles.editor}
        mode='julia'
        theme='dracula'
        onChange={handleChange}
        fontSize={16}
        showPrintMargin={true}
        highlightActiveLine={true}
        value={content}
        setOptions={{
          showLineNumbers: true,
          tabSize: 2
        }}
        wrapEnabled
        width='100%'
        height='calc(100% - 35px)'
      />
    </div>
  )
}

export default EditorArea
