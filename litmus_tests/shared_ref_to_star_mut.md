### Example

```rust
pub unsafe fn a() -> u8 {
    let mut x = 11;
    b(&x as *const u8 as *mut u8);
    x
}

unsafe fn b(x: *mut u8) {
    *x = 22;
}
```

### Explanation

Here the user takes a shared reference `&x` which is then cast to a
`*mut` reference and ater used to mutate the variable `x`. Subtle
aspects here:

- The lifetime of the `&x` reference will be inferred very short (just
  the duration of the cast, basically), so from a certain naive POV
  `x` is "not borrowed" and yet its value changes.
- The result of `&x` cannot, in safe code, be used to mutate `x`, and
  yet its value changes.
  
Based on either of the above points, one might think the function
above could return `11`, because the compiler might constant propagate
`11` from the `let mux x = 11` to the return value under the
assumption that it cannot change.

### Source

https://github.com/rust-lang/rust/issues/30424#issue-122623932
