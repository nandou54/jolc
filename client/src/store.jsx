import editorReducer from '@/reducers/editorReducer'
import outputReducer from '@/reducers/outputReducer'
import reportsReducer from '@/reducers/reportsReducer'
import { combineReducers, createStore } from 'redux'
import { composeWithDevTools } from 'redux-devtools-extension'
import appReducer from '@/reducers/appReducer'

const initialState = {
  app: { show: false },
  editorContent: localStorage.getItem('editorContent') || '/* get started */',
  reports: localStorage.getItem('reports') || {},
  output: []
}

const reducer = combineReducers({
  app: appReducer,
  editorContent: editorReducer,
  reports: reportsReducer,
  output: outputReducer
})

const store = createStore(reducer, initialState, composeWithDevTools())

export default store
