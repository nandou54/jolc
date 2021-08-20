const defaultState = { show: false }

const sideBarReducer = (state = defaultState, action) => {
  switch (action.type) {
    case '@sideBar/toggle': {
      const newState = { show: !state.show }
      return newState
    }
    default:
      return state
  }
}

export default sideBarReducer
