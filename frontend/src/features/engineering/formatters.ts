export function formatNumber(value: number): string {
  if (!Number.isFinite(value)) {
    return String(value);
  }
  if (Math.abs(value) >= 1e6 || (Math.abs(value) > 0 && Math.abs(value) < 0.001)) {
    return value.toExponential(4);
  }
  return value.toLocaleString(undefined, { maximumSignificantDigits: 6 });
}

export function formatValue(value: unknown): string {
  if (typeof value === 'number') {
    return formatNumber(value);
  }
  if (typeof value === 'string') {
    return value;
  }
  if (typeof value === 'boolean') {
    return value ? 'Yes' : 'No';
  }
  if (Array.isArray(value)) {
    return value.map(formatValue).join(', ');
  }
  if (value === null || value === undefined) {
    return 'Not available in current model';
  }
  return JSON.stringify(value);
}

export function labelize(key: string): string {
  return key.replace(/_/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
}
