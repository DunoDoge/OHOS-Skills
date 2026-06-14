// FunctionReturnTypeError.ets - annotate return types explicitly
class User {
  id: number = 0;
  name: string = '';
}

// BAD: inferred return type widens; downstream usage breaks
// function pickName(u) { return u?.name ?? 'anon'; }

// GOOD: explicit types everywhere
export function pickName(u: User | undefined): string {
  return u?.name ?? 'anon';
}

export function loadUser(id: number): Promise<User> {
  const u: User = new User();
  u.id = id;
  u.name = 'demo';
  return Promise.resolve(u);
}

export function logEvent(tag: string): void {
  console.info(tag);
}
