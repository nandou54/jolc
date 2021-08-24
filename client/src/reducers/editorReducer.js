const defaultState = ''
const editorReducer = (state = defaultState, action) => {
  switch (action.type) {
    case '@editor/update': {
      const newContent = action.payload
      save(newContent)
      return newContent
    }
    default:
      return state
  }
}

const save = (content) => localStorage.setItem('editor', content)

export default editorReducer
