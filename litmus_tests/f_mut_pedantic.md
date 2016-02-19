### Example

```rust
fn f_mut_pedantic<'s>(&'s mut self) -> &'s mut Self {
    let captured_self = self as *mut Self;
    unsafe { &mut *((&*captured_self).f() as *const Self as *mut Self) }
}
```

### Explanation

More explicit variation on
[f_mut_should_work.md](f_mut_should_work.md).  In particular, it's
important that the `f()` method here returns `self`. The tricky part
is that `self` is being converted from `&mut` to `&` and then back
again.

### Source

- https://github.com/rust-lang/rust/issues/30424#issuecomment-167009462
- https://github.com/rust-lang/rust/issues/30424#issuecomment-168539718
