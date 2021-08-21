const defaultState = {
  ast: [],
  errores: [],
  simbolos: []
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

const save = (reports) => localStorage.setItem('reports', reports)

export default reportsReducer
