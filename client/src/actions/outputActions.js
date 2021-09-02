const logOutput = (line) => ({
  type: '@output/log',
  payload: line
})

const appendOutput = (output) => ({
  type: '@output/append',
  payload: output
})

const clearOutput = () => ({
  type: '@output/clear'
})

export { logOutput, appendOutput, clearOutput }
