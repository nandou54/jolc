import { useEffect } from 'react'

function useKey(targetKey, callback, { ctrl = false, alt = false }, condition = true) {
  function handler({ key, ctrlKey, altKey }) {
    if (ctrl && !ctrlKey) return
    if (alt && !altKey) return
    if (key === targetKey) callback()
  }

  useEffect(() => {
    if (condition) {
      window.addEventListener('keydown', handler)
    } else {
      window.removeEventListener('keydown', handler)
    }
  }, [condition])
}

export default useKey
