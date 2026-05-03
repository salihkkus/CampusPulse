import { useState, useEffect, useRef, useCallback } from 'react';

// Global cache to store data between page navigations
const globalCache = new Map();

/**
 * Generic hook for fetching data from the API.
 * @param {Function} fetchFn  – async function that returns data
 * @param {Array}    deps     – dependency array for re-fetching
 * @param {number}   interval – auto-refresh interval in ms (0 = no refresh)
 */
export function useApi(fetchFn, deps = [], interval = 0) {
  // Use a stable cache key based on the function name + deps,
  // not the function reference (which changes every render for inline arrow fns)
  const cacheKey = `${fetchFn.name || 'anon'}_${JSON.stringify(deps)}`;

  const [data, setData] = useState(() => globalCache.get(cacheKey) || null);
  const [loading, setLoading] = useState(() => !globalCache.has(cacheKey));
  const [error, setError] = useState(null);

  // Keep latest fetchFn in a ref so the callback doesn't depend on it
  const fetchRef = useRef(fetchFn);
  fetchRef.current = fetchFn;

  // Track if the component is still mounted
  const mountedRef = useRef(true);
  useEffect(() => {
    mountedRef.current = true;
    return () => { mountedRef.current = false; };
  }, []);

  const load = useCallback(async () => {
    try {
      const result = await fetchRef.current();
      if (!mountedRef.current) return;
      setData(result);
      globalCache.set(cacheKey, result);
      setError(null);
    } catch (err) {
      if (!mountedRef.current) return;
      setError(err.message);
    } finally {
      if (mountedRef.current) setLoading(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cacheKey]);

  useEffect(() => {
    setLoading(prev => !globalCache.has(cacheKey) ? true : prev);
    load();
    if (interval > 0) {
      const id = setInterval(load, interval);
      return () => clearInterval(id);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [load, interval]);

  return { data, loading, error, reload: load };
}
