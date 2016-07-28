### Example

```rust
// Here the function (at the point of return)
// certainly has the right to write to the return
// pointer.
fn write_to_ret(condition: bool) -> Data {
    let f = get_data();
    if condition { abort(); }
    f
}

fn write_to_ref1(condition: bool, result: &mut Data) {
    let f = get_data();
    if condition { abort(); }
    *result = f;
}

fn write_to_ref2(condition: bool, result: &mut Data) {
    let f = get_data();
    if condition {
        /* something that does not abort but does not panic */
    }
    *result = f;
}

fn write_to_raw1(condition: bool, result: *mut Data) {
    let f = get_data();
    if condition { abort(); }
    unsafe { *result = f; } // maybe not, did not observe a write
}

fn write_to_raw1a(condition: bool, result: &mut Data) {
    let f = get_data();
    if condition { abort(); }
    *result = f; // but not this
    
    let f = get_data();
    if condition { abort(); }
    *result = f; // can NRVO this one
}

fn write_to_raw2(condition: bool, result: *mut Data) {
    let result = unsafe { &mut *result };
    let f = get_data();
    if condition { abort(); }
    *result = f;
}

fn write_to_raw3(condition: bool, result: *mut Data) {
    let f = get_data();
    if condition { abort(); }
    unsafe { *result = f; }

    let result = &mut * result; // this cannot "be moved"
    let f = get_data();
    if condition { abort(); }
    *result = f; // can only be promoted as high as the `&mut *result`
}
```

### Explanation

In all of these examples, there is a `let f = get_data()` and `f` is
then later re-used. The question is whether we could eliminate the
stack temporary and write the result of `get_data()` directly into its
eventual location. The danger typically arises because that write
would be visible (potentially) earlier than it was "supposed" to
happen -- when is that ok?

These examples mostly include a conditional abort in between: the
assumption is that the compiler understands that abort *aborts* and
does not return.

Some factors that are relevant:

- could other threads observe?


### Source

Where did this example come from?
