import { useState, useEffect } from 'react';

/**
 * Custom hook to debounce rapidly changing values (e.g., search and filter inputs).
 * Prevents unnecessary network requests and race conditions.
 * @param {*} value The value to debounce
 * @param {number} delay Delay in milliseconds (default: 300ms)
 * @returns {*} Debounced value
 */
export function useDebounce(value, delay = 300) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

export default useDebounce;

