### Example

#### Variation 1: all safe fns

```rust
fn escape_as_usize(x: &i32) -> usize {
    x as *const _ as usize
}

fn consume_from_usize(x: usize) -> i32 {
    let y: &i32 = unsafe { std::mem::transmute(x as *const i32) };
    *y
}

fn main() {
    let x = 2;
    let p = escape_as_usize(&x);
    println!("{}", consume_from_usize(p));
}
```

#### Variation 2: unsafe fns

```rust
fn escape_as_usize(x: &i32) -> usize {
    x as *const _ as usize
}

unsafe fn consume_from_usize(x: usize) -> i32 {
    let y: &i32 = unsafe { std::mem::transmute(x as *const i32) };
    *y
}

fn main() {
    let x = 2;
    let p = escape_as_usize(&x);
    unsafe {
        println!("{}", consume_from_usize(p));
    }
}
```

### Explanation

In this example, a reference is converted from a `&T` to a `usize` (by
`escape_as_usize`) and then converted back to `*const T` and
dereferenced (by `consume_from_usize`). The question is: under what
circumstances (if any) is this pattern legal?

Relevant optimization: we would [like to be able to infer][nocap] from
the signature of `escape_as_usize` that its argument is not captured.

The difference between the two examples is solely in the safety
declarations. In the first variant, `consume_from_usize` is declared
as a safe function. This is semantically incorrect, because in fact it
cannot accept any `usize` as argument. Rather, its inputs must meet
very specific criteria (it must be a valid pointer that can be
dereferenced). Nonetheless, the user has incorrectly put an unsafe
block in the body, rather than in the signature, and so the compiler
accepts this code. In the second variant, `consume_from_usize` is
correctly marked as `unsafe` to account for that.

If the first variant is legal, then we are very limited in our ability
do ["nocapture" optimizations][nocap]. The second variant might offer
a kind of escape hatch, where we are limited in our ability to do
optimizations but only within some sort of surrounding "unsafe scope"
-- but this may be too subtle for users, who do not currently view
unsafe as being semantically meaningful in this way (and of course
this scope must be carefully defined).

[nocap]: ../optimizations/nocapture_by_safe_fn.md

### Source

doener on IRC
