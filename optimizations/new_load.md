### Example

```rust
// When, if ever, can the compiler rewrite this:
fn foo(_x: &u64) { }

// Into this:
fn foo(x: &u64) {
   let _ = *x;
}
```

### Explanation

A variant of the [extra_load.md][] litmus test. See that example for
further discussion.

[extra_load.md]: ../litmus_tests/extra_load.md

### Source

https://internals.rust-lang.org/t/volatile-and-sensitive-memory/3188/9
