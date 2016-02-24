### Example

```rust
fn foo(x: &i32) -> usize {
    x as *const _ as usize
}

fn bar(x: usize) -> i32 {
    let y: &i32 = unsafe { std::mem::transmute(x as *const i32) };
    *y
}

fn main() {
    let x = 2;
    println!("{}", bar(foo(&x)));
}
```

### Explanation

In this example, the value `x` is cast to a `usize` and then
transmitted to `bar`, which then casts back to a pointer.  `bar` is
declared as a safe function: strictly speaking, this seems
semantically incorrect, because in fact it cannot accept any `usize`
as argument. Rather, its inputs must meet very specific criteria (it
must be a valid pointer that can be dereferenced). Nonetheless, the
user has incorrectly put an unsafe block in the body, rather than in
the signature, and so the compiler accepts this code.

Either something in this example must be UB or else we have to be
**very** limited in our ability to add "nocapture" annotations.  See
the ["nocapture by safe fn"][nocap] example for further thoughts.

[nocap]: ../optimizations/nocapture_by_safe_fn.md

### Source

doener on IRC
