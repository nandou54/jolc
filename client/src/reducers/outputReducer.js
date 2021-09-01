const outputReducer = (state = [], action) => {
  switch (action.type) {
    case '@output/log': {
      const newOutput = [...state, action.payload]
      return newOutput
    }
    case '@output/newOutput': {
      const newOutput = action.payload
      return newOutput
    }
    default:
      return state
  }
}

export default outputReducer
