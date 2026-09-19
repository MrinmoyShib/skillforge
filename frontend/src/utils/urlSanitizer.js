export function sanitizeUrl(url) {
  if (!url) return null;
  const trimmed = url.trim();
  if (/^https?:\/\//i.test(trimmed)) return trimmed;
  if (/^(javascript|data|vbscript):/i.test(trimmed)) return null;
  return `https://${trimmed}`;
}
