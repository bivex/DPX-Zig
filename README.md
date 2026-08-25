# ⚡ DPX-Zig: Systems Architecture, Comptime Generics, Allocator RAII, SIMD & GoF 23 Static Analyzer

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zig Version](https://img.shields.io/badge/Zig-0.11%20--%200.14+-F7A41D?logo=zig&logoColor=black)](https://ziglang.org)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Architecture: Hexagonal DDD](https://img.shields.io/badge/Architecture-Hexagonal%20DDD-blueviolet)](https://alistair.cockburn.us/hexagonal-architecture/)
[![CLI: Typer & Rich](https://img.shields.io/badge/CLI-Typer%20%26%20Rich-009688)](https://typer.tiangolo.com)
[![SARIF OASIS v2.1.0](https://img.shields.io/badge/SARIF-OASIS%20v2.1.0-blue)](https://sarifweb.azurewebsites.net)

**DPX-Zig** is an enterprise-grade static analysis engine and architectural pattern detector for Zig codebases. Engineered for **Low-Level Systems Programming, High-Performance Game Engines, Kernel/OS Runtimes, Embedded Hardware, Audio DSP, and Compilers**, it audits **Explicit Allocator Passing (`std.mem.Allocator`), Defer & Errdefer RAII Cleanup, Error Unions (`!T`, `try`/`catch`), Comptime Metaprogramming (`fn (comptime T: type) type`, `@typeInfo`), Tagged Unions (`union(enum)`), Packed & Extern Structs, SIMD Hardware Vectors (`@Vector`), Inline Assembly (`asm volatile`), all 23 GoF Design Patterns**, and **Zig Memory Safety Hazards (Missing Defer Deinit, Silent Error Catching, Unreachable Panics, Raw Pointer Alignment Risks)**.

[Features](#-key-features) • [Installation](#-installation) • [CLI Usage](#-cli-usage) • [Supported Rules](#-supported-pattern-rules--checks) • [The DPX Suite Family](#-the-dpx-suite-family)

</div>

---

## 🌟 Key Features

- ⚙️ **Explicit Allocator Discipline:** Verifies `allocator: std.mem.Allocator` parameter passing across APIs, eliminating hidden control flow and undocumented heap allocations.
- 🛡️ **Deterministic RAII Cleanup (`defer` / `errdefer`):** Identifies resource cleanup and multi-step transaction rollback semantics.
- ⚡ **Comptime Generic Metaprogramming:** Inspects compile-time type generators (`fn (comptime T: type) type`), `@typeInfo(T)` reflection, static assertions (`@compileError`), and unrolled loops (`inline for`).
- 🚀 **SIMD & Hardware Systems Acceleration:** Analyzes `@Vector(N, T)` intrinsics, direct CPU machine instructions (`asm volatile`), and C ABI interoperability (`@cImport`).
- 🏛️ **100% Complete Gang of Four (GoF 23/23):** Comprehensive detection of all 23 classic Creational, Structural, and Behavioral patterns adapted for Zig's struct composition, VTables, and tagged unions.
- 🚨 **Resilience & Memory Safety Hazards:** Flags unhandled empty `catch {}` error swallowing, missing `defer deinit()` memory leaks, `unreachable` statements in production, and unsafe `@ptrCast` / `@alignCast`.
- 📊 **Interactive Architecture Observability HUD:** Zero-dependency interactive HTML dashboard with instant search, KPI breakdown, and built-in **`🤖 Copy AI Context Prompt`** generator for LLMs (Claude, GPT-4, Gemini).
- 🔒 **CI/CD & GitHub Security Ready:** Standardized **OASIS SARIF v2.1.0**, JSON, and Markdown reports.

---

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/bivex/DPX-Zig.git
cd DPX-Zig

# Install dependencies using uv or pip
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

---

## 💻 CLI Usage

### 1. Scan a Zig Project or Package
```bash
# Terminal scan with Rich formatting
dpx-zig scan /path/to/zig/project

# Export Interactive HTML Observability HUD
dpx-zig scan src/ -H reports/zig_hud.html

# Generate AI Context Prompt for LLMs
dpx-zig scan src/ --llm

# Filter for specific Allocator or Comptime rules
dpx-zig scan src/ -p explicit_allocator_passing -p comptime_generic_type_function

# Export SARIF for GitHub Code Scanning
dpx-zig scan src/ -S reports/results.sarif
```

### 2. Inspect Supported Architectural Rules
```bash
dpx-zig rules
```

### 3. Query Deep Pattern Documentation
```bash
dpx-zig info explicit_allocator_passing
dpx-zig info comptime_generic_type_function
```

---

## 📋 Supported Pattern Rules & Checks

### 1. ⚙️ Zig Idiomatic & Systems Architecture
- `explicit_allocator_passing`: Explicit `allocator: std.mem.Allocator` passing without hidden allocations.
- `defer_errdefer_raii`: Deterministic resource cleanup with `defer` and `errdefer`.
- `error_union_try_catch`: Explicit error sets and error unions (`!T`) with `try`/`catch`.
- `tagged_union_exhaustive_switch`: Type-safe sum types (`union(enum)`) decomposed via exhaustive `switch`.
- `packed_extern_struct_layout`: Hardware bitfield packing (`packed struct`) or C ABI compatibility (`extern struct`).
- `opaque_type_c_handle`: Encapsulated foreign/C handles declared as `opaque {}`.

### 2. 🔮 Comptime & Metaprogramming
- `comptime_generic_type_function`: Zero-cost generic type generation functions (`fn (comptime T: type) type`).
- `comptime_typeinfo_reflection`: Compile-time type introspection and reflection via `@typeInfo(T)`.
- `comptime_static_assertion`: Compile-time constraint verification via `@compileError` or `@compileLog`.
- `inline_for_while_expansion`: Unrolled compile-time loop evaluation via `inline for` or `inline while`.

### 3. 🏎️ SIMD, Concurrency & Low-Level Hardware
- `simd_vector_acceleration`: Hardware vector parallelism utilizing `@Vector(N, T)` intrinsics.
- `inline_assembly_intrinsic`: Direct CPU instruction execution via `asm volatile`.
- `c_interop_translate_c`: Seamless C header translation via `@cImport` and `@cInclude`.

### 4. 🏛️ GoF Creational Patterns (5/5)
- `singleton_global_instance`: Comptime or global singleton coordinator.
- `factory_init_allocator`: Struct constructor function (`.init(allocator, ...)`) allocating resources.
- `abstract_factory_vtable_interface`: VTable-based interface returning polymorphic driver/allocator families.
- `builder_configuration_flow`: Method chaining struct builder pattern returning `Self`.
- `prototype_comptime_clone`: Deep struct cloning via allocator (`.clone(allocator)`).

### 5. 🧱 GoF Structural Patterns (7/7)
- `adapter_wrapper_type`: Struct wrapping foreign types or C ABI structs.
- `bridge_vtable_driver`: Decoupling domain logic from platform hardware drivers via VTable dispatch.
- `composite_recursive_tagged_union`: Recursive tree/AST node structures in tagged unions.
- `decorator_allocator_wrapper`: Wrapping an Allocator or Stream with logging/checking middleware.
- `facade_root_module_api`: Unified module entrypoint (`root.zig`) exposing cohesive public namespaces.
- `flyweight_static_intern_pool`: Sharing immutable pre-allocated terms, string tables, or slab pools.
- `proxy_vtable_gateway`: VTable proxy controlling access, locks, or buffering calls.

### 6. 🎯 GoF Behavioral Patterns (11/11)
- `chain_of_responsibility_pipeline`: Linked handler structs forwarding requests along a chain.
- `command_tagged_action_payload`: Tagged union command variants holding executable payloads.
- `interpreter_ast_switch_eval`: Evaluating domain AST expressions via exhaustive `switch`.
- `iterator_struct_next`: Structs implementing idiomatic `fn next(self: *Self) ?T`.
- `mediator_event_bus`: Central coordinator mediating communication between decoupled components.
- `memento_state_snapshot`: Capturing immutable state snapshot for checkpointing and rollback.
- `observer_callback_subscription`: Registry of subscriber callback function pointers or listener slices.
- `state_machine_tagged_union_fsm`: Finite State Machine transitions dispatched via tagged union states.
- `strategy_function_pointer_injection`: Passing interchangeable algorithm function pointers.
- `template_method_skeleton_hooks`: Algorithm skeleton coordinating steps with optional lifecycle hooks.
- `visitor_switch_payload_walker`: Visitor pattern traversing heterogeneous tagged union nodes with `switch`.

### 7. 🛡️ Safety, Memory & Concurrency Hazards
- `unhandled_error_union_catch_hazard`: Silent suppression of errors via `_ = func() catch {}`.
- `missing_defer_deinit_leak`: Allocating memory without a matching `defer deinit()` / `defer free()`.
- `unreachable_panic_in_production`: `unreachable` or `@panic()` in reachable production code paths.
- `raw_pointer_alignment_hazard`: Unchecked `@ptrCast` or `@alignCast` without alignment verification.

### 8. 📐 SOLID & Systems Clean Code
- `monolithic_struct_srp`: Struct declaring excessive fields (>= 12), violating Single Responsibility.
- `fat_vtable_interface_isp`: VTable struct declaring excessive function pointers (>= 10), violating ISP.
- `manual_type_switch_ocp`: Massive switch statement (>= 8 prongs); consider comptime or polymorphic dispatch.

---

---

## 🌐 The DPX Multi-Language Static Analysis Family (33 Languages)

| # | Language | Repository | Ecosystem & Focus |
|:---:|---|---|---|
| 1 | **Ada** | [`bivex/DPX-Ada`](https://github.com/bivex/DPX-Ada) | Ada 2012/2022, SPARK Contracts, Ravenscar Tasking, DO-178C Safety |
| 2 | **Clojure** | [`bivex/DPX`](https://github.com/bivex/DPX) | Lisp S-Expressions, Protocols, Multimethods |
| 3 | **C** | [`bivex/DPX-C`](https://github.com/bivex/DPX-C) | Memory Safety, Struct VTables, Idiomatic C11/C23 |
| 4 | **Cairo** | [`bivex/DPX-Cairo`](https://github.com/bivex/DPX-Cairo) | Starknet Smart Contracts, ZK-Rollup Invariants |
| 5 | **C++** | [`bivex/DPX-Cpp`](https://github.com/bivex/DPX-Cpp) | RAII, CRTP, Concepts, Modern C++20/23 |
| 6 | **C#** | [`bivex/DPX-CSharp`](https://github.com/bivex/DPX-CSharp) | .NET 9, Roslyn AST, Linq, Records |
| 7 | **Dart** | [`bivex/DPX-Dart`](https://github.com/bivex/DPX-Dart) | Dart 3.x, Flutter, BLoC, Riverpod, Isolates |
| 8 | **Elixir** | [`bivex/DPX-Elixir`](https://github.com/bivex/DPX-Elixir) | BEAM OTP, GenServer, Supervisors |
| 9 | **Erlang** | [`bivex/DPX-Erlang`](https://github.com/bivex/DPX-Erlang) | Fault Tolerance, Actor Model, OTP Behaviors |
| 10 | **Gleam** | [`bivex/DPX-Gleam`](https://github.com/bivex/DPX-Gleam) | Type-Safe BEAM, Actor Concurrency |
| 11 | **Go** | [`bivex/DPX-Go`](https://github.com/bivex/DPX-Go) | Goroutines, Channels, Composition, Interfaces |
| 12 | **Haskell** | [`bivex/DPX-Haskell`](https://github.com/bivex/DPX-Haskell) | Pure Functional, Monads, Typeclasses, Arrows |
| 13 | **Huff** | [`bivex/DPX-Huff`](https://github.com/bivex/DPX-Huff) | Low-Level EVM Bytecode & Opcodes |
| 14 | **Idris 2** | [`bivex/DPX-Idris2`](https://github.com/bivex/DPX-Idris2) | Dependent Types, QTT Linear Protocols, Totality, Proofs |
| 15 | **Java** | [`bivex/DPX-Java`](https://github.com/bivex/DPX-Java) | Spring Boot, Enterprise Java, JVM Invariants |
| 16 | **Julia** | [`bivex/DPX-Julia`](https://github.com/bivex/DPX-Julia) | Multiple Dispatch, Scientific Computing |
| 17 | **Kotlin** | [`bivex/DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin) | Coroutines, Multiplatform, Functional DSLs |
| 18 | **Lua** | [`bivex/DPX-Lua`](https://github.com/bivex/DPX-Lua) | Metatables, Coroutines, LuaJIT, Neovim |
| 19 | **Mojo** | [`bivex/DPX-Mojo`](https://github.com/bivex/DPX-Mojo) | SIMD Hardware, Memory Lifetimes, AI Systems |
| 20 | **Move** | [`bivex/DPX-Move`](https://github.com/bivex/DPX-Move) | Aptos & Sui Resource Safety, Linear Types |
| 21 | **OCaml** | [`bivex/DPX-OCaml`](https://github.com/bivex/DPX-OCaml) | Algebraic Data Types, Functors, Polymorphism |
| 22 | **PHP** | [`bivex/DPX-Php`](https://github.com/bivex/DPX-Php) | Modern PHP 8.4, Attributes, Traits, Laravel |
| 23 | **Prolog** | [`bivex/DPX-Prolog`](https://github.com/bivex/DPX-Prolog) | ISO Prolog, SWI-Prolog, DCG, CLP(FD/R/Q), CHR, Meta-Interpreters |
| 24 | **Puppet** | [`bivex/DPX-Puppet`](https://github.com/bivex/DPX-Puppet) | Puppet DSL, Roles/Profiles, IaC Security, Hiera |
| 25 | **Python** | [`bivex/DPX-Py`](https://github.com/bivex/DPX-Py) | Metaprogramming, Protocols, Hexagonal DDD |
| 26 | **Ruby** | [`bivex/DPX-Ruby`](https://github.com/bivex/DPX-Ruby) | Ruby 3.x, Rails, Metaprogramming, Dry-RB, Security |
| 27 | **Rust** | [`bivex/DPX-Rust`](https://github.com/bivex/DPX-Rust) | Zero-Cost Abstractions, Borrow Checker, Traits |
| 28 | **Solidity** | [`bivex/DPX-Solidity`](https://github.com/bivex/DPX-Solidity) | DeFi Security, Reentrancy, EVM Yul/Assembly |
| 29 | **SQL** | [`bivex/DPX-SQL`](https://github.com/bivex/DPX-SQL) | PostgreSQL, MySQL, SQLite, T-SQL, PL/SQL |
| 30 | **Swift** | [`bivex/DPX-Swift`](https://github.com/bivex/DPX-Swift) | Protocol-Oriented Programming, Actors |
| 31 | **TypeScript** | [`bivex/DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript) | Generics, Conditional Types, Clean Architecture |
| 32 | **Yul** | [`bivex/DPX-Yul`](https://github.com/bivex/DPX-Yul) | EVM Intermediate Representation Optimization |
| 33 | **Zig** | [`bivex/DPX-Zig`](https://github.com/bivex/DPX-Zig) | Comptime, Manual Memory Allocators, C ABI |

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
