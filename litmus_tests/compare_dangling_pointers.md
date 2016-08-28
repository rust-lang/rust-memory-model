### Example

```rust
fn compare_dangling_pointers()
{
    let p1: *const i32;
    {
        let x = Box::new(0);
        p1 = &*x;
    }
    {
        let y = Box::new(0);
        let p2: *const _ = &*y;
        let b = p1 == p2;
        println!("Are they equal? {} {}", b, p1 == p2);
    }
}
```

### Explanation

In C, once an object is deallocated, all pointers to it have an
indeterminate value. Hence the value of `p1` would be indeterminate
here. But it is accessible in safe Rust.

However, LLVM has a [different model][sunfish1], where it thinks only
about "aliasing". In other words, even if two pointers are equal, they
might be considered not to alias, in the case that one of them is
invalidated. This makes the above code perfectly legal.

[sunfish1]: https://internals.rust-lang.org/t/comparing-dangling-pointers/3019/22?u=nikomatsakis

### Source

https://internals.rust-lang.org/t/comparing-dangling-pointers/3019
