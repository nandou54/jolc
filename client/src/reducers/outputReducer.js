const outputReducer = (state = [], action) => {
  switch (action.type) {
    case '@output/log': {
      const newOutput = [...state, action.payload]
      return newOutput
    }
    case '@output/append': {
      const newOutput = [...state, ...action.payload]
      return newOutput
    }
    case '@output/clear': {
      const newOutput = []
      return newOutput
    }
    default:
      return state
  }
}

export default outputReducer
