const defaultState = { show: false, loading: false, content: '' }

const appReducer = (state = defaultState, action) => {
  switch (action.type) {
    case '@app/show': {
      const newState = { show: true, loading: state.loading }
      return newState
    }
    case '@app/hide': {
      const newState = { show: false, loading: state.loading }
      return newState
    }
    case '@app/toggleLoading': {
      const newState = { show: state.show, loading: !state.loading }
      return newState
    }
    default:
      return state
  }
}

export default appReducer
