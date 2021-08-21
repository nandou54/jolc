const editorReducer = (state = '', action) => {
  switch (action.type) {
    case '@editor/updateContent': {
      const newEditorContent = action.payload
      save(newEditorContent)
      return newEditorContent
    }
    default:
      return state
  }
}

const save = (editorContent) => localStorage.setItem('editorContent', editorContent)

export default editorReducer
