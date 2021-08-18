import editorContentReducer from '@/reducers/editorContentReducer'
import outputReducer from '@/reducers/outputReducer'
import { combineReducers, createStore } from 'redux'
import { composeWithDevTools } from 'redux-devtools-extension'
import sideBarReducer from '@/reducers/SideBarReducer'

const initialState = {
  editorContent: localStorage.getItem('editorContent') || '/* get started */',
  output: [],
  sideBar: { show: true, activePage: '/' }
}

const reducer = combineReducers({
  editorContent: editorContentReducer,
  output: outputReducer,
  sideBar: sideBarReducer
})

const store = createStore(reducer, initialState, composeWithDevTools())

export default store
