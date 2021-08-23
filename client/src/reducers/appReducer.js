const defaultState = { show: false, loading: false, content: '' }

const appReducer = (state = defaultState, action) => {
  switch (action.type) {
    case '@app/toggleSideBar': {
      const newState = { show: action.payload, loading: state.loading }
      return newState
    }
    case '@app/toggleLoading': {
      const newState = { show: state.show, loading: action.payload }
      return newState
    }
    default:
      return state
  }
}

export default appReducer
