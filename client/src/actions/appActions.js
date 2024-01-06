const toggleSideBar = (payload) => ({
  type: '@app/toggleSideBar',
  payload
})

const toggleLoading = (payload) => ({
  type: '@app/toggleLoading',
  payload
})

const changeSelectedTab = (payload) => ({
  type: '@app/changeSelectedTab',
  payload
})

const toggleAboutModal = (payload) => ({
  type: '@app/toggleAboutModal',
  payload
})

export { toggleSideBar, toggleLoading, changeSelectedTab, toggleAboutModal }
