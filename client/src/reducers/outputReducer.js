const outputReducer = (state = '', action) => {
  switch (action.type) {
    case '@output/newOutput': {
      const newOutput = [...state, action.payload]
      return newOutput
    }
    default:
      return state
  }
}

export default outputReducer
