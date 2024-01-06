const defaultState =
  localStorage.getItem('editor') || 'println("hello, world!");'

const editorReducer = (state = defaultState, action) => {
  switch (action.type) {
    case '@editor/update': {
      const newContent = action.payload
      try {
        save(newContent)
      } catch {
        console.log('Error al guardar el código localmente')
      }
      return newContent
    }
    default:
      return state
  }
}

const save = (content) => localStorage.setItem('editor', content)

export default editorReducer
