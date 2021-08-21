const showSideBar = () => ({
  type: '@app/show'
})

const hideSideBar = () => ({
  type: '@app/hide'
})

const toggleLoading = () => ({
  type: '@app/toggleLoading'
})

export { showSideBar, hideSideBar, toggleLoading }
