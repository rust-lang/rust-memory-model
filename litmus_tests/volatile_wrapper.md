### Example

What is the proper FFI declaration and/or Rust equivalent to the following:

```C
struct Foo {
    volatile uint8_t buffer[64];
};
```

Or, on a related note, does a wrapper like the following suffice to
ensure that all accesses to `x` are "volatile acesses"?

```rust
pub struct VolatileCell<T> {
     x: T
}
impl<T> VolatileCell<T> {
    pub fn get(&self) -> T {
        unsafe {
            ptr::read_volatile(&self.x)
        }
    }
    pub fn set(&mut self, x: T) {
        unsafe {
            ptr::write_volatile(&mut self.x, x)
        }
    }
}
```

### Explanation

Rust's current APIs and types do not include a way to declare volatile
lvalues. We do have volatile pointer accesses. This model is
[inherited from LLVM][llvm]. LLVM in particular does not seem to have
a notion of volatile objects. [Quoting @briansmith][b-llvm]:

> Anyway, I did some research and I learned more about how LLVM
> works. Basically, AFAICT, LLVM doesn't keep track of which objects
> are volatile and which ones aren't.  Instead, it just doesn't touch
> anything unless it is touched by a non-volatile load or non-volatile
> store. But, once a non-volatile load or non-volatile store is seen,
> it feels free to start optimizing those loads/stores which might
> result in a load/store getting moved to a different point in the
> program than it appears in the program's source.

However, the C spec itself seems to have a notion of
[volatile objects][b], though there full details are [complex][c-lv]
and [not entirely clear][pc]. What model do we wish to adopt here?

Of particular importance is the question of
[synthesizing new loads][new_load.md] -- if the compiler can create
loads out of thin air (rather than duplicating existing loads that it
can prove exist), then it seems that some notion of "volatile storage"
is required. Otherwise, it is sufficient to use an abstraction like
the one shown.

Another related question is whether changing `x` to use `UnsafeCell<T>`
affects the answer.

Also related, particular for Brian Smith's concerns, is the question
of whether the compiler can guarantee that memory is
[deinitialized from the stack and/or registers][deinit].

### Source

- https://internals.rust-lang.org/t/volatile-and-sensitive-memory/3188/20
- https://internals.rust-lang.org/t/volatile-and-sensitive-memory/3188/6

[extra_load.md]: extra_load.md
[llvm]: https://internals.rust-lang.org/t/volatile-and-sensitive-memory/3188/8
[c-lv]: https://internals.rust-lang.org/t/volatile-and-sensitive-memory/3188/11
[pc]: https://internals.rust-lang.org/t/volatile-and-sensitive-memory/3188/13
[am]: https://internals.rust-lang.org/t/volatile-and-sensitive-memory/3188/26
[b]: https://internals.rust-lang.org/t/volatile-and-sensitive-memory/3188/27
[b-llvm]: https://internals.rust-lang.org/t/volatile-and-sensitive-memory/3188/33
[deinit]: https://internals.rust-lang.org/t/volatile-and-sensitive-memory/3188/34?u=nikomatsakis
