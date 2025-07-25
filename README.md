# lazy-state-machine

This repository contains an implementation of a programmable finite state machine (FSM).

This implementation accepts a transition function which is a general-purpose Python function.

I chose this approach because while understanding how the rules for a modulus-3 state machine were derived,
I noticed the rules table grows very quickly with modulus number, and I ran out of
memory when I tried to obtain the table for a 64-bit number. The name `lazy-state-machine`
was chosen because it allows for rules to be derived on-demand instead of pretabulated.

Accepting a Python function in the FSM also allows for computing nondeterminism.

In practice accepting a Python function makes the machines hard to analyze,
and in production code where possible I would want to use a transition table
and draw it out in a nice diagram.

## Code Structure

* `lazy_state_machine/exceptions.py` - Errors the machine can generate representing various misconfigurations or transition function misbehaviors
* `lazy_state_machine/lazy_state_machine.py` - The state machine, which is configured on `__init__` and is immutable, accepting inputs through three different functions for different purposes
* `tests/test_invalid_inputs.py` - Cases where each of the exceptions would be triggered
* `tests/test_modulus.py` - My first use of the FSM, and where I explored the derivation of modulus rules
* `tests/test_turnstile.py` - A second example
* `examples/FSM_modulus_three.py` - A standalone modulus three demonstration
* `examples/schrodingers_cat.py` - A little fun example of nondeterminism, and a FSM's state after processing a provided input not being in the accepted final states

The tests provide complete coverage.

## Running Examples

The examples depend on the `lazy_state_machine` library. Run them from the repository root using `uv`:

```bash
uv run --with . examples/FSM_modulus_three.py
uv run --with . examples/schrodingers_cat.py
```

## Development Setup

To develop on this library, it can also be installed into the system Python via the traditional approach:

```bash
pip install -e .
```

## Building and Distribution

The package can be built as a wheel with `make build` and installed into any other python environment via:

```bash
pip install /path/to/lazy-state-machine/dist/lazy_state_machine-*.tar.gz
```

If this were code I was intending on seriously releasing as an open source project, or using commercially, I would continue with the steps in TODO.md.

## Development Tools

I used a tool called cookiecutter to add tooling to this repo according to a predefined template.
I chose the template [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv) which
uses the python package manager uv, to experiment with it.

The template provides the following options; the coverage I added.

* `make install` - Install the dependencies (they are all development dependencies, no special libraries are needed to use the library)
* `make check` - Linters (formatting, code smells, typing)
* `make test` - Testing though pytest
* `make coverage` - Testing through pytest with code coverage, generated as html in a folder `htmlcov`
* `make build` - Create a distributable python package (wheel)
* `make clean-build` - Clean the build files after running `make build`

## Installation Requirements

Please note that if you don't have `uv` already installed, it can be installed with any of the following on Linux or MacOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
pip install uv
pipx install uv
```

On windows it can be installed with:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

If on windows, make can be installed via instructions on this page:
https://gnuwin32.sourceforge.net/packages/make.htm