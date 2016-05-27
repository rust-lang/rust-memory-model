### Example

```rust
impl [T] {
    pub fn split_at_mut(&mut self, mid: usize) -> (&mut [T], &mut [T]) {
        let copy: &mut [T] = unsafe { mem::transmute_copy(&self) };
        let left = &mut self[0..mid];
        let right = &mut copy[mid..];
        (left, right)
    }
}
```

### Explanation

it cheats the compiler by "duplicating" `self` using the unsafe
function [`transmute_copy`][transmute_copy]. This means that both
`self` and `copy` are `&mut [T]` slices pointing at the same memory,
at the same time. In ordinary, safe Rust, this is impossible, but
using `transmute_copy`, we can make it happen.

The rest of the function looks almost the same as our original attempt
at a safe implementation (also in the [previous post][pp]). The only
difference now is that, in defining `right`, it uses `copy[mid..]`
instead of `self[mid..]`. The compiler accepts this because it assumes
that `copy` and `self`, since they are both simultaneously valid, must
be disjoint (remember that, in unsafe code, the borrow checker still
enforces its rules on safe typess, it's just that we can use tricks
like raw pointers or transmutes to sidestep them).

So this raises a question -- is this legal unsafe code to write, given
that it is only accepted because the borrowck thinks (incorrectly)
that `self` and `copy` are disjoint?

### Source

Rust sources (this was how `split_at_mut` was originally written).
