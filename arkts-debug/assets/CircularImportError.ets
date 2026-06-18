// CircularImportError.ets - extract shared types to break circular imports
// NOTE: This single file demonstrates the anti-pattern and the fix.
// In a real project, each section would be in its own file.

// ============================================================
// BAD: circular imports between moduleA and moduleB
// ============================================================
// --- moduleA.ets ---
// import { formatUser } from './moduleB';   // A imports B
// export interface User { id: number; name: string; }
// export function processUser(u: User): string { return formatUser(u); }

// --- moduleB.ets ---
// import { User } from './moduleA';          // B imports A → cycle!
// export function formatUser(u: User): string { return `User: ${u.name}`; }

// ============================================================
// GOOD: extract shared types into a separate module
// ============================================================
// --- shared/types.ets ---
interface User {
  id: number;
  name: string;
}

// --- moduleA.ets (would import from shared/types) ---
export function processUser(u: User): string {
  return u.name;
}

// --- moduleB.ets (would import from shared/types) ---
export function formatUser(u: User): string {
  return `User: ${u.name}`;
}

export { User, processUser, formatUser };
