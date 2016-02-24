### Example

```rust
fn escape_simple(x: &i32) -> usize {
    22
}

fn escape_as_usize(x: &i32) -> usize {
    x as usize
}

fn escape_as_ptr(x: &i32) -> *const i32 {
    x
}

fn escape_as_another_ptr(x: &i32) -> *const u32 {
    x as *const u32
}

pub struct MyType(*const i32);

fn escape_as_newtype(x: &i32) -> MyType {
    MyType(x)
}

fn escape_as_vec(x: &i32) -> Vec<i32> {
    ...
}
```

### Explanation

To be very LLVM specific, we'd like to add "nocapture" attributes.
More generally, we'd like to be able to assume that if you have an
argument of type `fn foo<'a>(x: &'a T) -> U`, and `'a` (nor any
lifetime related to `'a`) does not appear in `U`, then we can assume
that no alias of `x` escapes `foo`. However, it's not clear that we
can always assume that.

- `escape_simple` -- no capture would be appropriate.
- `escape_as_usize` -- same types as previous example, but in this case
  one might imagine that the user expects to coerce the result back to
  a pointer and use it. Is that legal?
- `escape_as_ptr` -- same as above, but they were more explicit in their types.
- `escape_as_another_ptr` -- same as above, but the type of the pointer does not
  match.
- `escape_as_newtype` -- same as above, but there is a newtype wrapping this
  `*const`. The question here is: if we have some type-based rules that examine
  the return value, how deeply do we delve? See also next example.
- `escape_as_vec` -- variant on the previous case where it seems like
  we should be able to assume nocapture, even though the return type
  contains a `*const i32`.

See also the the ["usize transfer"][ut] litmus test for further
discussion, and in particular for examples that show the callers
involved.

[ut]: ../litmus_tests/usize_transfer.md

### Source

IRC conversation: https://botbot.me/mozilla/rustc/2016-02-24/?msg=60823650&page=1
