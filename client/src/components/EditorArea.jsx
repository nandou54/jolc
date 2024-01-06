import styles from '@/styles/EditorArea.module.css'
import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import AceEditor from 'react-ace'

import { updateContent } from '@/actions/editorActions'

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
      <AceEditor
        className={styles.editor}
        mode="julia"
        theme="dracula"
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
        width="100%"
        height="100%"
      />
    </div>
  )
}

export default EditorArea
