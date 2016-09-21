This repository is intended to help us develop a coherent and clear
set of "unsafe code guidelines" for Rust. The goal of these guidelines
is to make it clear what kinds of actions unsafe can legally take
and what it cannot.

A crucial part (but not the only part) of these guidelines
is a "memory model" that tries to define what kind of aliasing
and accesses unsafe code can perform (this in turn implies
limitations on the transformations and optimizations the compiler can do).

We're still in the 'data gathering' stage of this effort. Most of the action
is taking place in the GitHub issues attached to this repository.

There are issues that describe numerous kinds of things, tagged with K- labels:

- `K-Model`: indicates a proposed "high-level model" for some aspect of unsafe code. Basically a set of rules that declares what is legal and not.
- `K-Code-Example`: some code that may or may not be legal when evaluated against a particular model
- `K-Optimization`: something the compiler may or may not be able to do when evaluated against a particular model
- `K-Task`: something that we have to do, such as investigating certain things and creating new issues if necessary
- `K-Related-Work`: a concise summary of some bit of related work, with links to learn more

### Files

The files in the repository are from a somewhat older phase and ought to be migrated to issues. =)

### Contributions

All the contents of this repository are licensed under the same terms as the Rust source itself (MIT/Apache2). Participation in the repository is assumed to imply agreement with these terms.
