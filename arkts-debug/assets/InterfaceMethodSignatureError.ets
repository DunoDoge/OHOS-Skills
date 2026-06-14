// InterfaceMethodSignatureError.ets - prefer property syntax with arrow types
// BAD: method-syntax interface vs property-syntax literal
// interface Handlers {
//   onLoad(id: number): void;
// }
// const h: Handlers = { onLoad: (id: number) => {} }; // signature mismatch

// GOOD: property syntax in both interface and literal
interface Handlers {
  onLoad: (id: number) => void;
  onError: (err: Error) => void;
}

export const h: Handlers = {
  onLoad: (id: number): void => {
    console.info(`load ${id}`);
  },
  onError: (err: Error): void => {
    console.error(err.message);
  }
};
