"""Domain CodeModel entities representing Zig AST, structs, unions, and functions."""

from __future__ import annotations

from dataclasses import dataclass, field
from pattern_detector.domain.value_objects import SourceLocation


@dataclass
class ZigField:
    """Field declaration in a Zig struct, union, or enum."""

    name: str
    type_name: str
    is_comptime: bool = False
    is_pub: bool = False
    location: SourceLocation | None = None


@dataclass
class ZigStruct:
    """Struct declaration in Zig (struct, packed struct, extern struct, opaque)."""

    name: str
    kind: str = "struct"  # "struct", "packed struct", "extern struct", "opaque"
    is_pub: bool = False
    is_generic: bool = False
    fields: list[ZigField] = field(default_factory=list)
    methods: list[ZigFunction] = field(default_factory=list)
    location: SourceLocation | None = None
    raw_text: str = ""

    @property
    def is_vtable(self) -> bool:
        return "VTable" in self.name or any("fn(" in f.type_name or "*const fn" in f.type_name for f in self.fields)

    @property
    def total_fields_count(self) -> int:
        return len(self.fields)


@dataclass
class ZigUnion:
    """Union declaration in Zig (tagged or untagged)."""

    name: str
    is_tagged: bool = False
    tag_type: str = ""  # e.g. "enum" or "enum(u8)"
    is_pub: bool = False
    fields: list[ZigField] = field(default_factory=list)
    location: SourceLocation | None = None
    raw_text: str = ""


@dataclass
class ZigEnum:
    """Enum declaration in Zig."""

    name: str
    is_pub: bool = False
    tag_type: str = "auto"
    fields: list[str] = field(default_factory=list)
    location: SourceLocation | None = None


@dataclass
class ZigParam:
    """Function parameter in Zig."""

    name: str
    type_name: str = "anytype"
    is_comptime: bool = False


@dataclass
class ZigFunction:
    """Function declaration in Zig (pub fn, fn, inline fn, export fn)."""

    name: str
    is_pub: bool = False
    is_export: bool = False
    is_inline: bool = False
    is_generic: bool = False
    parameters: list[ZigParam] = field(default_factory=list)
    return_type: str = "void"
    body: str = ""
    defers_count: int = 0
    errdefers_count: int = 0
    tries_count: int = 0
    catches_count: int = 0
    switches_count: int = 0
    branch_count: int = 1
    has_unreachable: bool = False
    has_panic: bool = False
    has_simd: bool = False
    has_inline_asm: bool = False
    has_ptrcast: bool = False
    has_typeinfo: bool = False
    location: SourceLocation | None = None
    raw_text: str = ""

    @property
    def accepts_allocator(self) -> bool:
        return any("Allocator" in p.type_name or p.name == "allocator" for p in self.parameters)


@dataclass
class ZigImport:
    """Import statement in Zig (@import(...) or @cImport(...))."""

    path_or_pkg: str
    alias: str | None = None
    is_c_import: bool = False
    location: SourceLocation | None = None


@dataclass
class ZigFile:
    """Parsed single Zig source file (.zig)."""

    file_path: str
    raw_content: str
    lines: list[str] = field(default_factory=list)
    imports: list[ZigImport] = field(default_factory=list)
    structs: list[ZigStruct] = field(default_factory=list)
    unions: list[ZigUnion] = field(default_factory=list)
    enums: list[ZigEnum] = field(default_factory=list)
    functions: list[ZigFunction] = field(default_factory=list)


@dataclass
class CodeModel:
    """Aggregated structural model of a scanned Zig codebase."""

    target_path: str = ""
    files: list[ZigFile] = field(default_factory=list)

    @property
    def all_structs(self) -> list[ZigStruct]:
        return [s for f in self.files for s in f.structs]

    @property
    def all_unions(self) -> list[ZigUnion]:
        return [u for f in self.files for u in f.unions]

    @property
    def all_enums(self) -> list[ZigEnum]:
        return [e for f in self.files for e in f.enums]

    @property
    def all_functions(self) -> list[ZigFunction]:
        return [fn for f in self.files for fn in f.functions]

    @property
    def all_imports(self) -> list[ZigImport]:
        return [imp for f in self.files for imp in f.imports]
