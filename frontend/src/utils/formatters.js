export function formatXP(xp) {
  if (xp === null || xp === undefined) return '0';
  return xp.toLocaleString();
}

export function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

export function formatDuration(seconds) {
  if (seconds === null || seconds === undefined) return '0s';
  if (seconds < 1) return `${(seconds * 1000).toFixed(0)}ms`;
  return `${seconds.toFixed(2)}s`;
}
