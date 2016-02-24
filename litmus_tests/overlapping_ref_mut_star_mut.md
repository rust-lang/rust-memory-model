### Example

```rust
fn foo(x: &mut i32) {
  let y = x as *mut _;
  *x = 41;
  unsafe { *y = 42; }
}
```

### Explanation

Both `x` and `y` are live and usable at the same time, but `x` is
`&mut`. The borrow checker is happy because `x` is implicitly reborrow
when it is cast to `*mut`, and that reborrow lasts for an extremely
short duration: only the cast itself!

Key questions:

- Under what scope (if any) can `y` be used legally?

### Source

https://github.com/rust-lang/rust/issues/30424#issuecomment-171294294
