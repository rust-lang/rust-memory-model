### Example

The `Ref` and `RefMut` types taken from `core::cell::RefCell`:

```rust
pub struct Ref<'b, T: ?Sized + 'b> {
    value: &'b T,
    borrow: BorrowRef<'b>,
}

pub struct RefMut<'b, T: ?Sized + 'b> {
    value: &'b mut T,
    borrow: BorrowRefMut<'b>,
}
```

### Explanation

What is interesting about these types are the `value` fields. They use
a normal Rust type, but in fact the guarantees for this are slightly
weaker than normal: the reference is valid until either (a) the end of
`'b` OR (b) the field `borrow` is dropped, whichever happens
first. This means that the type *appears* entirely "safe", but in fact
there are extra requirements, which speaks to the idea of an "unsafety
frontier" that is also explored in other litmus tests such as
[usize_transfer][].

### Source

An email from Ralf Jung.

[usize_transfer]: usize_transfer.md
