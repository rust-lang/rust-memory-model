### Example

```rust
fn f(&self) -> &Self { self }
fn f_mut_should_work<'s>(&'s mut self) -> &'s mut Self {
    let ret = unsafe { &mut *(self.f() as *const Self as *mut Self) };
    ret // β-expansion should have no effect
}
```

(In the case of a compiler transform, include the transformed source
code as well.)

### Explanation

- `self` is borrowed only within the unsafe block
  - on second line, both `ret` and `self` are live mutable pointers to the same place.
  
Could be considered UB because multiple invalid aliases are *in
scope*, but then they are never used. See also
[f_mut_unsure.md](f_mut_unsure.md).

### Source

https://github.com/rust-lang/rust/issues/30424#issuecomment-167009014

