This repository is intended to help us develop a coherent and clear
"memory model" for Rust. The goal of a memory model specifically is to
define:

- what kinds of aliasing and accesses unsafe code can perform;
- what kinds of transformations and optimizations the compiler can do.

This in turn implies the kinds of things that unsafe code can rely on.

We're still in the 'data gathering' stage of this effort. Therefore,
this repository currently consists of a series of examples scraped
from various comment threads. Each example is defined by a markdown
file based on `template.md`. These examples are broken into two
categories:

- `litmus_tests` -- bits of unsafe code that someone might write;
  eventually, we may decide that some of these bits of unsafe code are
  illegal and hence might trigger undefined behavior.
- `optimizations` -- transformations the compiler might want to
  perform; eventually, we may decide that some of these bits of unsafe
  code are illegal and hence the compiler could not do them.

Naturally these two things are in tension. That is, the more
optimizations the compiler can do, the fewer litmus tests will be
legal. Eventually, it would be nice to have a chart indicating which
tests are in conflict with which optimizations.


