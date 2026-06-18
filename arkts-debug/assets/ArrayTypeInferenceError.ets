// ArrayTypeInferenceError.ets - always specify explicit element types for arrays

// BAD: missing element type in array declaration
// class MyClass {
//   public a: [][] = [];           // no inner type
//   public b: number[][] = [];     // this is OK
//   public c: [] = [];             // no element type at all
// }

// GOOD: explicit element types
class MyClass {
  public a: string[][] = [];
  public b: number[][] = [];
  public c: string[] = [];
}

// GOOD: single-dimensional arrays with explicit types
const names: string[] = [];
const counts: number[] = [];
const flags: boolean[] = [];

export { MyClass, names, counts, flags };
