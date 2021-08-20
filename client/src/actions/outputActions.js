const log = (line) => ({
  type: '@output/log',
  payload: line
})

const newOutput = (output) => ({
  type: '@output/newOutput',
  payload: output
})

export { log, newOutput }
