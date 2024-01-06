const defaultState = {
  ast: '',
  errors: [],
  symbols: { variables: [], functions: [], structs: [] },
  c3d: ''
}

const reportsReducer = (state = defaultState, action) => {
  switch (action.type) {
    case '@reports/update': {
      const newReports = action.payload
      return newReports
    }
    default:
      return state
  }
}

export default reportsReducer
