### Example

```
#[derive(Debug,Copy,Clone)]
struct Foo {
    bar: Bar
}
#[derive(Debug,Copy,Clone)]
struct Bar {
    // lots of data
}
fn doit() -> u32 {
    let foo = Foo { bar: make_bar() };
    debug!("{}", &foo);
    match foo {
        Foo { bar } => frobnicate(&mut bar)
    };
}
```

### Explanation

In the function `doit`, we would like the compiler to be able to make
`bar` binding point to `foo.bar` in place. But if the `debug!` macro
should cast the `&foo` to `*const Foo` and keep a reference, it could
observe the change. Is it allowed to do that?

### Source

https://github.com/rust-lang/rust/issues/30424#issuecomment-167009462

