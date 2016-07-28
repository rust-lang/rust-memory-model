### Example

```rust
// Here the function (at the point of return)
// certainly has the right to write to the return
// pointer.
fn write_to_ret(condition: bool) -> Data {
    let f = get_data();
    XXX
    f
}

fn write_to_ref(condition: bool, result: &mut Data) {
    let f = get_data();
    XXX
    *result = f;
}

fn write_to_raw1(condition: bool, result: *mut Data) {
    let f = get_data();
    XXX
    unsafe { *result = f; } // maybe not, did not observe a write
}

fn write_to_raw1a(condition: bool, result: &mut Data) {
    let f = get_data();
    XXX
    *result = f; // but not this
    
    let f = get_data();
    XXX
    *result = f; // can NRVO this one
}

fn write_to_raw2(condition: bool, result: *mut Data) {
    let result = unsafe { &mut *result };
    let f = get_data();
    XXX
    *result = f;
}

fn write_to_raw3(condition: bool, result: *mut Data) {
    let f = get_data();
    XXX
    unsafe { *result = f; }

    let result = &mut * result; // this cannot "be moved"
    let f = get_data();
    XXX
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

These examples include some unknown behavior XXX in between. Typically
speaking, whether the optimization can be performed will depend (in
each case) on what this XXX is:

- For example, it may contain a *conditional abort*. In that case, if
  we optimize the write to occur early, we don't know that the write
  would even ever execute!
- Similarly, if XXX might unwind, that could lead to potential reads
  of the ultimate destination, in some cases. 
- Finally, the XXX might read from the ultimate destination through an
  alias (in some cases, that read may be considered undefined
  behavior, however).


### Source

Where did this example come from?
