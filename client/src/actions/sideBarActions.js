const toggleSideBar = () => ({
  type: '@sideBar/toggle'
})

const navigateSideBar = (to) => ({
  type: '@sideBar/navigate',
  payload: to
})

export { toggleSideBar, navigateSideBar }
