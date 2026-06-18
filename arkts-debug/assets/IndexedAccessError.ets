// IndexedAccessError.ets - use dot notation or Map instead of bracket notation

interface Config {
  host: string;
  port: number;
}

const config: Config = { host: 'localhost', port: 8080 };

// BAD: indexed access with bracket notation
// const host = config['host'];       // arkts-no-props-by-index
// const key = 'port';
// const port = config[key];          // arkts-no-props-by-index

// GOOD 1: dot notation for known properties
export const host: string = config.host;
export const port: number = config.port;

// GOOD 2: Map for dynamic key-value lookups
const headers: Map<string, string> = new Map();
headers.set('Content-Type', 'application/json');
headers.set('Accept', 'application/json');

export function getHeader(key: string): string | undefined {
  return headers.get(key);
}
