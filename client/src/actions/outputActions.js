const logOutput = (payload) => ({
  type: '@output/log',
  payload: payload
})

const appendOutput = (payload) => ({
  type: '@output/append',
  payload
})

const clearOutput = () => ({
  type: '@output/clear'
})

export { logOutput, appendOutput, clearOutput }
