const defaultState = { show: false, loading: false, showAboutModal: false }

const appReducer = (state = defaultState, action) => {
  switch (action.type) {
    case '@app/toggleSideBar': {
      const newState = {
        ...state,
        show: action.payload,
        loading: state.loading
      }
      return newState
    }
    case '@app/toggleLoading': {
      const newState = { ...state, show: state.show, loading: action.payload }
      return newState
    }
    case '@app/toggleAboutModal': {
      const newState = { ...state, showAboutModal: action.payload }
      return newState
    }
    default:
      return state
  }
}

export default appReducer
