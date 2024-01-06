import { combineReducers, createStore } from 'redux'

import appReducer from '@/reducers/appReducer'
import outputReducer from '@/reducers/outputReducer'
import editorReducer from '@/reducers/editorReducer'
import reportsReducer from '@/reducers/reportsReducer'

const reducer = combineReducers({
  app: appReducer,
  output: outputReducer,
  editor: editorReducer,
  reports: reportsReducer
})

const store = createStore(reducer)

export default store
