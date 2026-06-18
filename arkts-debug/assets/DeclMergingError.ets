// DeclMergingError.ets - consolidate declarations instead of merging

// BAD: declaration merging
// interface User {
//   name: string;
// }
// interface User {
//   age: number;    // arkts-no-decl-merging
// }

// BAD: namespace merging
// namespace Utils {
//   export function foo(): void {}
// }
// namespace Utils {
//   export function bar(): void {}  // arkts-no-decl-merging
// }

// GOOD 1: single consolidated declaration
interface User {
  name: string;
  age: number;
}

// GOOD 2: use extends to build on a base interface
interface UserBase {
  name: string;
}

interface DetailedUser extends UserBase {
  age: number;
  email: string;
}

// GOOD 3: single namespace with all exports
namespace Utils {
  export function foo(): void {}
  export function bar(): void {}
}

export { User, DetailedUser, Utils };
