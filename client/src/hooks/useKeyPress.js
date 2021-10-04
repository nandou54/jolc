import { useEffect } from 'react'

function useKeyPress(targetKey, callback, { ctrl = false } = {}) {
  const handlePress = ({ key, ctrlKey }) => {
    if (key === targetKey && (!ctrl || (ctrl && ctrlKey))) {
      callback()
    }
  }

  useEffect(() => {
    window.addEventListener('keydown', handlePress)
    return () => {
      window.removeEventListener('keydown', handlePress)
    }
  }, [callback])
}

export default useKeyPress
