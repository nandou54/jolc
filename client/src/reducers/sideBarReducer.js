const defaultState = { show: false, activePage: '/' }

const sideBarReducer = (state = defaultState, action) => {
  switch (action.type) {
    case '@sideBar/toggle': {
      const newState = { show: !state.show, activePage: state.activePage }
      return newState
    }
    case '@sideBar/navigate': {
      const newState = { show: state.show, activePage: action.payload }
      return newState
    }
    default:
      return state
  }
}

export default sideBarReducer
