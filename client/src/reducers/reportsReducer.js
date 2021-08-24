const defaultState = {
  ast: [],
  errors: [],
  symbols: []
}

const reportsReducer = (state = defaultState, action) => {
  switch (action.type) {
    case '@reports/update': {
      const newReports = action.payload
      save(newReports)
      return newReports
    }
    default:
      return state
  }
}

const save = (reports) => localStorage.setItem('reports', JSON.stringify(reports))

export default reportsReducer
