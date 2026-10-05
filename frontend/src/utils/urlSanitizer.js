export function sanitizeUrl(url) {
  if (!url || typeof url !== 'string') return null;
  // Strip control characters and whitespace
  const clean = url.replace(/[\u0000-\u001F\u007F-\u009F\s]/g, '');
  if (!clean) return null;

  // Reject protocol-relative URLs
  if (clean.startsWith('//')) return null;

  try {
    const candidate = /^https?:\/\//i.test(clean) ? clean : `https://${clean}`;
    const parsed = new URL(candidate);
    if (parsed.protocol === 'http:' || parsed.protocol === 'https:') {
      return parsed.href;
    }
  } catch {
    return null;
  }
  return null;
}
