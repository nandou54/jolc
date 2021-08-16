import React, { useEffect, useState } from 'react'
import styles from '@/styles/EditorArea.module.css'

import AceEditor from 'react-ace'
import axios from 'axios'

import { useSelector, useDispatch } from 'react-redux'

// import 'ace-builds/src-noconflict/theme-dracula'
// import 'ace-builds/src-noconflict/ext-language_tools'
// import 'ace-builds/src-noconflict/ext-beautify'
import { updateEditorContent } from '@/actions/editorContentActions'

function EditorArea() {
  const editorContent = useSelector((state) => state.editorContent)
  const dispatch = useDispatch()

  // useEffect(async () => {
  //   const result = await axios.post('http://127.0.0.1:8000/api', { text: '2+2' })
  //   console.log(result)
  //   // setContent(result)
  // }, [])

  const handleChange = (newEditorContent) => {
    dispatch(updateEditorContent(newEditorContent))
  }

  return (
    <div className={styles.base}>
      <AceEditor
        className={styles.editor}
        // theme='dracula'
        onChange={handleChange}
        fontSize={18}
        showPrintMargin={true}
        showGutter={true}
        highlightActiveLine={true}
        value={editorContent}
        setOptions={{
          showLineNumbers: true,
          tabSize: 2,
          cursorStyle: 'wide',
          useSoftTabs: true
        }}
        width='100%'
        height='100%'
      />
    </div>
  )
}

export default EditorArea
