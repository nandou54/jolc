const toggleSideBar = (payload) => ({
  type: '@app/toggleSideBar',
  payload
})

const toggleLoading = (payload) => ({
  type: '@app/toggleLoading',
  payload
})

const toggleAboutModal = (payload) => ({
  type: '@app/toggleAboutModal',
  payload
})

export { toggleSideBar, toggleLoading, toggleAboutModal }
