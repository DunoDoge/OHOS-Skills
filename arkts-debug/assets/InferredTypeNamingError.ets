// InferredTypeNamingError.ets - add explicit return type annotations for exported symbols

interface Config {
  host: string;
  port: number;
}

// BAD: inferred return type cannot be named without reference to internal type
// export function createConfig() {
//   return { host: 'localhost', port: 8080 };  // inferred type is not portable
// }

// GOOD 1: explicit return type annotation
export function createConfig(): Config {
  return { host: 'localhost', port: 8080 };
}

// GOOD 2: use a named type alias for complex return types
type ConfigOrError = Config | string;

export function loadConfig(): ConfigOrError {
  return { host: 'localhost', port: 8080 };
}

// GOOD 3: explicit return type for async functions
export async function fetchConfig(): Promise<Config> {
  return { host: 'localhost', port: 8080 };
}
