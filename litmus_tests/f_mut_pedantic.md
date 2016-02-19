### Example

```
fn f_mut_pedantic<'s>(&'s mut self) -> &'s mut Self {
    let captured_self = self as *mut Self;
    unsafe { &mut *((*captured_self).f() as *const Self as *mut Self) }
}
```

### Explanation

More explicit variation on [f_mut_should_work.md](f_mut_should_work.md).

### Source

https://github.com/rust-lang/rust/issues/30424#issuecomment-167009462
