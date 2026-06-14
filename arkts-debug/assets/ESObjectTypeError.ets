// ESObjectTypeError.ets - replace ESObject with a concrete interface
// BAD: leaking ESObject into typed code
// const u: ESObject = nativeUser.getCurrent();
// console.info(u.name); // type error / arkts-no-esobject

// GOOD: declare an interface that matches the actual native shape
interface NativeUser {
  id: number;
  name: string;
}

interface NativeUserModule {
  getCurrent: () => NativeUser;
}

// Pretend this comes from a native ESModule binding.
declare const nativeUser: NativeUserModule;

export function readNativeUser(): string {
  const u: NativeUser = nativeUser.getCurrent();
  return u.name;
}
