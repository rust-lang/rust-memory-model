Some terms, defined by me. Please debate on them, or correct them, as you see fit :)

* Object - Contiguous block of memory with a certain size and a certain alignment.

Each object has the capability to read the memory.

Not all objects have the capability of writing the memory.

An object may be allocated in static memory:

```rust
static x: i32 = 0i32; // a static, read-only object of size >= 4, alignment >= 4
static mut x: i32 = 0i32; // a static, read-write object of size >= 4, alignment >= 4
static x: AtomicI32 = 0i32; // a static, read-write object of size >= 4, alignment >= 4
```

or on the stack:

```rust
let x: i32 = 0i32; // a stack, read-only object of size >= 4, alignment >= 4
// you get the point
```

or on the heap:

```rust
let x: Box<i32> = Box::new(0i32); // a stack, read-only object pointing to a heap,
                                  // read-write object of size >= 4, alignment >= 4
```

* `lexpr` or `locator expression` - A typed expression which refers to a specific memory location, an object, as opposed to just a value - i.e., if you try to move it, and it's not Copy, there's a compiler error

If you read a lexpr of type T, the object referred to by the lexpr must have `align_of::<T>()`, and `size_of::<T>()`. The bytes of the object gets read as the type of the lexpr, if they are valid; otherwise, undefined behavior.

```rust
let x: Box<i32> = Box::new(0i32);
-> x
-> *x
```

Both examples of expressions that refer to specific objects.

* `value` - A typed expression which refers only to a value - i.e., if you take the address, it must create a temporary.

```rust
-> 0i32
let x: i32 = 0i32;
-> &x
```

A note:

Objects aren't typed. No, not even effective types ^-^
