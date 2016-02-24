### Example

```rust
fn caller(x: &mut i32) {
    callee(x, x);
}

fn callee(x: *mut i32, y: *mut i32) {
}

fn main() { }
```

### Explanation

In the call to `callee`, there is an implicit reborrow of `x` and
coercion of the resulting reborrow to a `*mut`. These reborrows have a
very short lifetime, so here we can coerce `x` twice into a `*mut`.

Since this pattern occurs everywhere in FFI libraries, this suggests
that if we coerce an `&'a mut` (resp. `&'a`) to a `*mut/*const`
(resp. `*const`), we should not say that the resulting unsafe pointer
is only usable during `'a`, because `'a` may be something unreasonably
short.

### Source

https://github.com/rust-lang/rust/issues/30424#issuecomment-171344268
