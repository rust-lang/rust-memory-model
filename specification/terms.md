## Statics

### Type

A rustc `Ty` - You should know what this is :-). Not to be confused with an LLVM type or anything else.

### Concrete Type

A *type* without type parameters. The memory model concerns only *concrete types*.

### Location Expression (lexpr)


A typed expression that evaluates to an *object*, as opposed to a *vexpr*. The LHS of an assignment and the scrutinee of a pattern are examples of *lexpr*s.

If a *vexpr* is used where an *lexpr* is expected (other than the LHS of an assignment, where
using a *vexpr* is illegal), it is wrapped in an implicit *temporary lexpr*.

### Value Expression (vexpr)

A typed expression that evaluates to an *value*, as opposed to a *lexpr*. The RHS of an
assignment and the arguments of a function are examples of *vexpr*s.

If a *lexpr* is used where an *vexpr* is expected, it is wrapped in an implicit
*use vexpr*.

### Temporary Lexpr

```Rust
    LExprKind::Temp(P<VExpr>)
```

A kind of implicit *lexpr* that wraps a *vexpr* when a *lexpr* is needed. When
 evaluated, it:

 * creates a temporary slot, scheduled for destruction at the end of the current *temporary scope*.
 * evaluates the *vexpr* and stores it within the slot.
 * evaluates into the temporary slot object.

A common example occurs when the result of `format!` is borrowed - it is wrapped by
an implicit temporary lexpr.

```Rust
fn send(message: &str) {
    /* .. */
}

fn main() {
    let message = &format!("1+1={}", 1+1);
    send(message);
}
```

### Use Vexpr

```Rust
    LExprKind::Use(P<LExpr>)
```

A kind of implicit *vexpr* that wraps a *lexpr* when a *vexpr* is needed. When
evaluated, it evaluates the *lexpr* and reads the *value* from the evaluated-to
*object*.

If the expression's type does not implement `Copy`, the value is moved out of the
read-from *object*, preventing further accesses.

The read-from *object* must be aligned to `align_of::<T>()` or behavior is undefined.

As usual, all `size_of::<T>()` bytes of the *object* must be accessible and
remain stable for the duration required by the aliasing rules.

### Lvalue, Rvalue

These terms are banned because they are used in conflicting ways in various places.

## Dynamics

### Object - Contiguous block of memory with a certain size and a certain alignment.

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

A note:

Objects aren't typed. No, not even effective types ^-^

### Value - inhabitant of a type

A *value* is the inhabitant of a type. *Value*s are purely mathematical objects and neither live in memory not form part of a program statement. However, datums may be partially `undef` (do we want that?).

Example values are `true: bool`, `[0, 0, 0, 0]: [u32; 4]`, `0xcccccccc: *const u32`, `the address of the local "foo": &u32`. `Some((4, 2)): Option<(u32, usize)>`.
