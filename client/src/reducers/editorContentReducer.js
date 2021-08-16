const editorContentReducer = (state = '', action) => {
  switch (action.type) {
    case '@editorContent/update': {
      const newEditorContent = action.payload
      save(newEditorContent)
      return newEditorContent
    }
    default:
      return state
  }
}

const save = (editorContent) => localStorage.setItem('editorContent', editorContent)

export default editorContentReducer
