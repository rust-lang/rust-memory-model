Some terms, defined by @ubsan and @arielb1. Please debate on them, or correct them, as you see fit :)

For explicitness, some of the section contain ADT declarations. These ADT declarations use Rust syntax for familiarity, but all smart pointers have been removed for clarity.

## §1 Types

A type is a construct in Rust which defines certain parameters, and which turns an array of bytes into a value.

A type may have type, lifetime, or (in the future) constant parameters. If any of these parameters are generic, then the type is a "generic type". Otherwise, the type is a "concrete type".

A type is any of the following:

### §1.1 Primitives

#### §1.1.1 Numeric types

 * `u8`
 * `u16`
 * `u32`
 * `u64`
 * `usize`
 * `i8`
 * `i16`
 * `i32`
 * `i64`
 * `isize`
 * `f32`
 * `f64`

#### §1.1.2 Pointers

 * `<T> *const T`
 * `<T> *mut T`
 * `<'a, T> &'a T`
 * `<'a, T> &'a mut T`

#### §1.1.3 Arrays

`<T, const N: usize> [T; N]`

#### §1.1.4 Slices

 * `str`
 * `<T> [T]`

#### §1.1.5 Tuples

 * `<T> (T,)`
 * `<T, U> (T, U)`
 ...

#### §1.1.6 Function Pointers

 * `fn()`
 * `<T, U> fn(T) -> U`
 ...


### §1.2 `struct`s

(TODO)

### §1.3 `enum`s

(TODO)

## §2 Expressions

### §2.1 Location Expressions (lexprs)

A typed expression that evaluates to an object, as opposed to a value. The LHS of an assignment and the examinee of a pattern are examples of lexprs.

If a vexpr is used where an lexpr is expected (other than the LHS of an assignment, where using a vexpr is illegal), it is wrapped in an implicit temporary lexpr, the rules of which are given in §2.3.

### §2.2 Value Expressions (vexprs)

A typed expression that evaluates to an value, as opposed to an object. The RHS of an assignment and the arguments of a function are examples of vexprs.

NOTE: Because of evaluation order concerns, after being potentially wrapped to a
vexpr, subexpressions are often wrapped in a `VExpr::Use(LExpr::Temp(vexpr))`. The
exact rules here should be documented.

If a lexpr is used where an vexpr is expected, it is wrapped in an implicit use
vexpr, the rules of which are given in §2.3.

### §2.3 Temporary lexpr

```Rust
    LExpr::Temp(VExpr)
```

An implicit lexpr that wraps a vexpr when an lexpr is expected.
 When evaluated, it:

 * creates a temporary object, scheduled for destruction at the end of the current temporary scope.
 * evaluates the vexpr and stores it within the object.
 * evaluates to the temporary object.

A common example occurs when the result of `format!` is borrowed - it is wrapped by an implicit temporary lexpr.

```Rust
fn send(message: &str) {
    /* .. */
}

fn main() {
    let message = &format!("1+1={}", 1+1);
    send(message);
}
```

### §2.4 Use vexpr

```Rust
    VExpr::Use(LExpr)
```

An implicit vexpr that wraps a lexpr when a vexpr is expected.

When evaluated, it:

    * evaluates the lexpr to an object
    * reads the value from that object and evaluates to it.

If the value read is an `undef`, behavior is undefined unless the expression's
type is an integer, in which case behavior is unspecified (FIXME: this is intended
to allow reads from padding - what can we say here?).

The read-from object must be aligned to `align_of::<T>()` or behavior is undefined.

If the expression's type does not implement `Copy`, the value is moved out of the
object, preventing further accesses.

### §2.5 Destruction scopes

A Rust function always keeps a chain of destruction scopes. Each destruction scope contains a list of objects - temporaries and variables - that are to be destroyed when that scope is exited.

The objects in a scope are dropped in the reverse order of their insertion. If such an object is in an uninitialized state (either because it was never initialized or because it was moved out of), it is not destroyed again.

If one of the destructors panics, the current scope as well as the remaining scopes
are exited and the panic continues to unwind.

### §2.5.1 Temporary scopes

A set of baroque rules assigns a destruction scope, called the *temporary scope*,
to each expression.

FIXME: explain these rules.

The temporary created by `LExpr::Temp` is added to that expression's temporary
scope's destruction list.

### §2.6 Note on the terms lvalue and rvalue

These terms aren't used in this document, because they are used in conflicting ways in various places. However, lvalue is equivalent to lexpr, while rvalue is equivalent to vexpr.

## §3 Objects

An object is an untyped, contiguous block of memory with a certain size and a certain alignment.

### §3.1 Capabilities

All objects are able to be read, but you may not write to all objects.

A lexpr associated with an object, as a vexpr, will evaluate to a value (see §4) that is equivalent to the memory of the object, interpreted as the type of the lexpr.

A write to an object will set the memory of that object equivalent to the value of the write, without the interpretation of typing.

### §3.2 Allocation.

An object may be allocated in one of three ways:

In static memory:

```rust
static x: i32 = 0i32; // a static, read-only object of size >= 4, alignment >= 4
static mut x: i32 = 0i32; // a static, read-write object of size >= 4, alignment >= 4
static x: AtomicI32 = 0i32; // a static, read-write object of size >= 4, alignment >= 4
```

on the stack:

```rust
let x: i32 = 0i32; // a stack, read-only object of size >= 4, alignment >= 4
// you get the point
```

or on the heap:

```rust
let x: Box<i32> = Box::new(0i32); // a stack, read-only object pointing to a heap,
                                  // read-write object of size >= 4, alignment >= 4
```

### §3.3 Note on types:

Objects *are not* typed. No, not even effective types ^-^

## §4 Value

A value is a specific inhabitant of a type. Values are pure mathematical objects, and do not live in memory. They only exist to be stored in objects, and to be evaluated.

### §4.1 Examples

```rust
true
[0, 0, 0, 0]
0xcccccccc as *const u32
{
    let foo: u32 = 0;
    &foo // <-
}
Some((4u32, 2usize))
```

### §4.2 Undef

A special case of any value is "undef". Any type may take on the value "undef", excepting zero sized types. The act of storing "undef" is not UB.

### §4.3 Conversion to Memory

A value, in order to get stored into memory, must first undergo the process of transformation from pure mathematical object into a computer-friendly form. Memory shall be represented as a byte array. Integers will be converted to base-2, 2's complement; floats shall be converted to IEEE754; etc. Any padding shall take on the value "undef".

### §4.4 Conversion from Memory

Conversion from memory will be a conversion to memory, but in reverse, going from computer-friendly form to pure mathematical object.

## §5 Memory

### §5.1 Segmentation

Rust works on a flat address space - addresses are numbers between
`0` and `2^wordlen`. However, for semantic purposes, memory is divided into an
hierarchy of segments, each of which describes a contiguous set of addresses.

The addresses `0` and `2^wordlen-1` are not assigned to any segment. This prevents
segments from wrapping around the end of address space.

Coexisting segments may not overlap (unless one is the supersegment of another). However, segments may be added or removed at run-time, possibly through intrinsics that can be triggered from user code.

Segments have an identity - removing a segment and creating another with the same address-set does not result in the same segment.

During their lifetime, each stack allocation and global variable is contained within a single segment.

NOTE: segments are used to represent LLVM objects, and *not* Rust borrowed pointers.

Every stack allocation or global variable will contain only addresses for a single
segment. There MAY exist intrinsics that subdivide segments.

Every pointer or reference is associated with a segment. That segment follows
the pointer as it is stored and loaded from memory, and through projections.

Each of the `size_of::<T>()` bytes from the address of a reference to a type `T` must always be contained within that reference's segment.

When a raw pointer to type `T` is accessed, each of the `size_of::<T>()` bytes from
its address must be contained within its segment.
