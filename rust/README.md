# Rust

I'm using [`cargo-aoc`][cargo-aoc] to manage and run my Rust solutions.

## How to run?

First, install [`cargo-aoc`][cargo-aoc].

Put your input files in a folder `input/2021/` using the naming pattern
`dayX.txt` (or let `cargo-aoc` do it for you). Note that `X`, the day number, is
not allowed to contain leading zeros.

Then, to run day `X` and part `Y`, use:

```sh
cargo aoc -d X -p Y
```

[cargo-aoc]: https://github.com/gobanos/cargo-aoc
