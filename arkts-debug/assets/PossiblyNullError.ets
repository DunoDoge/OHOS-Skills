// PossiblyNullError.ets - guard nullable values before access
class User {
  id: number = 0;
  name: string = '';
  constructor(id: number, name: string) {
    this.id = id;
    this.name = name;
  }
}

function findUser(id: number): User | null {
  return id === 1 ? new User(1, 'Alice') : null;
}

// BAD: object possibly null
// const u = findUser(2);
// console.info(u.name);

// GOOD 1: explicit null check
export function readNameStrict(id: number): string {
  const u: User | null = findUser(id);
  if (u !== null) {
    return u.name;
  }
  return 'anon';
}

// GOOD 2: optional chaining with fallback
export function readNameLoose(id: number): string {
  const u: User | null = findUser(id);
  return u?.name ?? 'anon';
}

// GOOD 3: early return narrows the variable
export function logName(id: number): void {
  const u: User | null = findUser(id);
  if (u === null) { return; }
  console.info(u.name);
}
