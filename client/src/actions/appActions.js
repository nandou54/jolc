const toggleSideBar = (on) => ({
  type: '@app/toggleSideBar',
  payload: on
})
const toggleLoading = (on) => ({
  type: '@app/toggleLoading',
  payload: on
})

export { toggleSideBar, toggleLoading }
