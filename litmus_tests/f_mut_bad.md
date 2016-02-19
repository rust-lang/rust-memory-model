### Example

```rust
fn f_mut_bad<'s>(&'s mut self) -> &'s mut Self {
    let ret = unsafe { transmute::<&'s Self, &'s mut Self>(self.f()) };
    ret // β-expansion should have no effect
}
```

### Explanation

In this variation on the lovely and delightful `f_mut` series, the
`self.f()` point has a lifetime of `'s`, and thus the scope of the
shared borrow extends past the unsafe block.

### Source

- https://github.com/rust-lang/rust/issues/30424#issuecomment-168541165
