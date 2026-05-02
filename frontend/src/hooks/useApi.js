import { useState, useEffect, useCallback } from 'react';

/**
 * Generic hook for fetching data from the API.
 * @param {Function} fetchFn  – async function that returns data
 * @param {Array}    deps     – dependency array for re-fetching
 * @param {number}   interval – auto-refresh interval in ms (0 = no refresh)
 */
export function useApi(fetchFn, deps = [], interval = 0) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    try {
      const result = await fetchFn();
      setData(result);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, deps);

  useEffect(() => {
    load();
    if (interval > 0) {
      const id = setInterval(load, interval);
      return () => clearInterval(id);
    }
  }, [load, interval]);

  return { data, loading, error, reload: load };
}
