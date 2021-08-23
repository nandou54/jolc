import React from 'react'
import styles from '@/styles/EditorArea.module.css'

import { useSelector, useDispatch } from 'react-redux'
import { updateEditorContent } from '@/actions/editorActions'

import AceEditor from 'react-ace'
import 'ace-builds/src-noconflict/theme-dracula'

function EditorArea() {
  const editorContent = useSelector((state) => state.editorContent)
  const dispatch = useDispatch()

  const handleChange = (newEditorContent) => {
    dispatch(updateEditorContent(newEditorContent))
  }

  return (
    <div className={styles.base}>
      <div className={`${styles.title} unselectable`}>editor</div>
      <AceEditor
        className={styles.editor}
        theme='dracula'
        onChange={handleChange}
        fontSize={16}
        showPrintMargin={true}
        highlightActiveLine={true}
        value={editorContent}
        setOptions={{
          showLineNumbers: true,
          tabSize: 2
        }}
        width='100%'
        height='calc(100% - 35px)'
      />
    </div>
  )
}

export default EditorArea
