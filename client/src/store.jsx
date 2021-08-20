import editorReducer from '@/reducers/editorReducer'
import outputReducer from '@/reducers/outputReducer'
import { combineReducers, createStore } from 'redux'
import { composeWithDevTools } from 'redux-devtools-extension'
import sideBarReducer from '@/reducers/sideBarReducer'

const initialState = {
  editorContent: localStorage.getItem('editorContent') || '/* get started */',
  output: [],
  sideBar: { show: true }
}

const reducer = combineReducers({
  editorContent: editorReducer,
  output: outputReducer,
  sideBar: sideBarReducer
})

const store = createStore(reducer, initialState, composeWithDevTools())

export default store
