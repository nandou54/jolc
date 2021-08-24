import { combineReducers, createStore } from 'redux'
import { composeWithDevTools } from 'redux-devtools-extension'

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

const editor = localStorage.getItem('editor') || '/* get started */'

const reports = localStorage.getItem('reports')
  ? JSON.parse(localStorage.getItem('reports'))
  : { ast: [], errors: [], symbols: [] }

const initialState = {
  app: { show: false, loading: false },
  output: [],
  editor,
  reports
}

const store = createStore(reducer, initialState, composeWithDevTools())

export default store
