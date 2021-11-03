import { useEffect } from 'react'

function useKeyPress(targetKey, callback, { ctrl = false, alt = false } = {}) {
  callback ||= () => {}

  const handlePress = ({ key, ctrlKey, altKey }) => {
    if (ctrl && !ctrlKey) return
    if (alt && !altKey) return
    if (key === targetKey) callback()
  }

  useEffect(() => {
    window.addEventListener('keydown', handlePress)
    return () => window.removeEventListener('keydown', handlePress)
  }, [callback])
}

export default useKeyPress
