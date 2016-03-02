### Example

```rust
#![feature(core_intrinsics)]

fn easy(x: &u64, y: &u64) -> u64 {
    if *x != 0 {
        *x
    } else {
        *y
    }
}

fn easy_optimized(x: &u64, y: &u64) -> u64 {
    // The compiler replaces two loads of `*x`
    let ret = *x;
    if ret != 0 {
        ret
    } else {
        *y
    }
}

fn tricky(x: &u64, y: &u64) -> u64 {
    if unsafe { std::intrinsics::volatile_load(x as *const u64) } != 0 {
        unsafe { std::intrinsics::volatile_load(x as *const u64) }
    } else {
        *y
    }
}

fn tricky_extra_load(x: &u64, y: &u64) -> u64 {
    // The compiler adds a spurious read of `*x` when compiling `tricky`.
    let _ = *x;
    if unsafe { std::intrinsics::volatile_load(x as *const u64) } != 0 {
        unsafe { std::intrinsics::volatile_load(x as *const u64) }
    } else {
        *y
    }
}

fn main() {
  let x = 1;
  let y = 2;
  easy(&x, &y);
  easy_optimized(&x, &y);
  tricky(&x, &y);
  tricky_extra_load(&x, &y);
}
```

### Explanation

The question here is (partly) about the relationship between loads and
volatile loads. In particular, for security-sensitive code, there is a
desire to ensure that the compiler does not insert new loads of memory
that were not present in the original source. For example,
transforming `tricky` into `tricky_extra_load` can lead to one fewer
load than you would otherwise have.

In LLVM today, one can add a `dereferenceable` annotation, which
indicates that speculative reads may be safely inserted. It may make
sense to add `dereferenceable` for `&T` in some cases. If `x` were
marked with `dereferenceable` in `tricky`, that may in turn imply that
the compiler could transform it to `tricky_extra_load`, though this
would depend on the precise definition of `dereferenceable` -- for
example, is the compiler allowed to insert loads that do not in fact
occur within the source?  And, if so, would it ever do so?

### Source

https://internals.rust-lang.org/t/volatile-and-sensitive-memory/3188/3
