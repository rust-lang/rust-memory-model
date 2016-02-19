### Example

```rust
fn f(&self) -> &Self { self }
fn f_mut_unsure<'s>(&'s mut self) -> &'s mut Self {
    let ret = unsafe { transmute::<&Self, &'s mut Self>(self.f()) };
    ret // β-expansion should have no effect
}
```

### Explanation

- `self` is borrowed only within the unsafe block
  - on second line, both `ret` and `self` are live mutable pointers to the same place.
- reborrow of `self` would be another alias, alive just after the return from transmute
  - this is what is linted against
        
Under "instant death" rules, both are UB, so we can't have that.

Under the access-based rules, both are fine.

We had a proposal flying around that &-references use instant death
and &mut use some variant of access-based, which would make the first
UB and the second safe.

### Source

https://github.com/rust-lang/rust/issues/30424#issuecomment-167009014
