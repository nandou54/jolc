import React from 'react'
import styles from '@/styles/EditorArea.module.css'

import AceEditor from 'react-ace'

import { useSelector, useDispatch } from 'react-redux'

import 'ace-builds/src-noconflict/theme-dracula'
import 'ace-builds/src-noconflict/ext-language_tools'
import 'ace-builds/src-noconflict/ext-beautify'
import { updateEditorContent } from '@/actions/editorActions'

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
        fontSize={20}
        showPrintMargin={true}
        highlightActiveLine={true}
        value={editorContent}
        setOptions={{
          showLineNumbers: true,
          tabSize: 2,
          cursorStyle: 'wide',
          useSoftTabs: true
        }}
        width='100%'
        height='calc(100% - 35px)'
      />
    </div>
  )
}

export default EditorArea
