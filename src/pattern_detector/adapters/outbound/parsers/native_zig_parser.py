"""High-speed native parser adapter for Zig source code (.zig)."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import (
    CodeModel,
    ZigEnum,
    ZigField,
    ZigFile,
    ZigFunction,
    ZigImport,
    ZigParam,
    ZigStruct,
    ZigUnion,
)
from pattern_detector.domain.value_objects import SourceLocation
from pattern_detector.ports.outbound import ParserPort


def _split_top_level_commas(s: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for char in s:
        if char in "([{<":
            depth += 1
            current.append(char)
        elif char in ")]}>":
            depth -= 1
            current.append(char)
        elif char == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if current:
        parts.append("".join(current).strip())
    return [p for p in parts if p]


class NativeZigParserAdapter(ParserPort):
    """Single-pass robust parser extracting Zig AST semantics, structs, unions, and comptime functions."""

    IMPORT_PATTERN = re.compile(
        r"^\s*(?:pub\s+)?const\s+(?P<alias>[a-zA-Z0-9_]+)\s*=\s*@import\(\s*[\"'](?P<path>[^\"']+)[\"']\s*\)"
    )
    C_IMPORT_PATTERN = re.compile(
        r"^\s*(?:pub\s+)?const\s+(?P<alias>[a-zA-Z0-9_]+)\s*=\s*@cImport\("
    )
    STRUCT_HEADER = re.compile(
        r"^\s*(?P<pub>pub\s+)?const\s+(?P<name>[a-zA-Z0-9_]+)\s*=\s*(?P<kind>packed\s+struct|extern\s+struct|struct|opaque)\s*(?:\{|\()"
    )
    UNION_HEADER = re.compile(
        r"^\s*(?P<pub>pub\s+)?const\s+(?P<name>[a-zA-Z0-9_]+)\s*=\s*union(?:\((?P<tag>[^)]+)\))?\s*\{"
    )
    ENUM_HEADER = re.compile(
        r"^\s*(?P<pub>pub\s+)?const\s+(?P<name>[a-zA-Z0-9_]+)\s*=\s*enum(?:\((?P<tag>[^)]+)\))?\s*\{"
    )
    FN_PREFIX_PATTERN = re.compile(
        r"^\s*(?P<pub>pub\s+)?(?P<export>export\s+)?(?P<inline>inline\s+)?fn\s+(?P<name>[a-zA-Z0-9_]+)\s*\("
    )
    BRANCH_KEYWORDS = re.compile(r"=>|\bif\s*\(|\bwhile\s*\(|\bfor\s*\(|\bcatch\b|\btry\b")

    def _parse_params(self, params_str: str) -> list[ZigParam]:
        if not params_str.strip():
            return []

        params: list[ZigParam] = []
        for p_clean in _split_top_level_commas(params_str):
            is_comptime = "comptime " in p_clean
            clean_no_comptime = p_clean.replace("comptime ", "").strip()

            if ":" in clean_no_comptime:
                p_name, p_type = clean_no_comptime.split(":", 1)
                params.append(
                    ZigParam(
                        name=p_name.strip(),
                        type_name=p_type.strip(),
                        is_comptime=is_comptime,
                    )
                )
            else:
                params.append(
                    ZigParam(
                        name=clean_no_comptime,
                        type_name="anytype",
                        is_comptime=is_comptime,
                    )
                )
        return params

    def _parse_field(self, line: str, file_path: str, line_idx: int) -> ZigField | None:
        trimmed = line.strip().rstrip(",")
        if not trimmed or trimmed.startswith("//"):
            return None

        is_pub = trimmed.startswith("pub ")
        if is_pub:
            trimmed = trimmed[4:].strip()

        is_comptime = trimmed.startswith("comptime ")
        if is_comptime:
            trimmed = trimmed[9:].strip()

        if ":" in trimmed:
            f_name, f_type = trimmed.split(":", 1)
            # Remove default value if any e.g. f: u32 = 0
            if "=" in f_type:
                f_type = f_type.split("=", 1)[0]
            return ZigField(
                name=f_name.strip(),
                type_name=f_type.strip(),
                is_comptime=is_comptime,
                is_pub=is_pub,
                location=SourceLocation(file_path=file_path, line=line_idx, column=1),
            )
        return None

    def parse_file(self, file_path: str, content: str) -> ZigFile:
        lines = content.splitlines()
        file_obj = ZigFile(file_path=file_path, raw_content=content, lines=lines)

        current_struct: ZigStruct | None = None
        current_union: ZigUnion | None = None
        current_function: ZigFunction | None = None
        current_func_body: list[str] = []
        brace_depth = 0

        for line_idx, raw_line in enumerate(lines, 1):
            trimmed = raw_line.strip()

            # Skip comments and empty lines
            if trimmed.startswith("//") or not trimmed:
                continue

            # Imports
            c_imp = self.C_IMPORT_PATTERN.match(trimmed)
            if c_imp:
                file_obj.imports.append(
                    ZigImport(
                        path_or_pkg="c_headers",
                        alias=c_imp.group("alias"),
                        is_c_import=True,
                        location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                    )
                )
                continue

            imp_m = self.IMPORT_PATTERN.match(trimmed)
            if imp_m:
                file_obj.imports.append(
                    ZigImport(
                        path_or_pkg=imp_m.group("path"),
                        alias=imp_m.group("alias"),
                        is_c_import=False,
                        location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                    )
                )
                continue

            # Struct Start
            struct_m = self.STRUCT_HEADER.match(trimmed)
            if struct_m and not current_function and not current_struct and not current_union:
                is_pub = bool(struct_m.group("pub"))
                s_name = struct_m.group("name")
                s_kind = struct_m.group("kind").strip()

                current_struct = ZigStruct(
                    name=s_name,
                    kind=s_kind,
                    is_pub=is_pub,
                    location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                    raw_text=raw_line,
                )

                if "opaque" in s_kind or ("{" in trimmed and "}" in trimmed):
                    file_obj.structs.append(current_struct)
                    current_struct = None
                continue

            # Union Start
            union_m = self.UNION_HEADER.match(trimmed)
            if union_m and not current_function and not current_struct and not current_union:
                is_pub = bool(union_m.group("pub"))
                u_name = union_m.group("name")
                tag = union_m.group("tag")

                current_union = ZigUnion(
                    name=u_name,
                    is_tagged=bool(tag),
                    tag_type=tag or "",
                    is_pub=is_pub,
                    location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                    raw_text=raw_line,
                )

                if "{" in trimmed and "}" in trimmed:
                    file_obj.unions.append(current_union)
                    current_union = None
                continue

            # Inside Struct: Accumulate fields or close
            if current_struct and not current_function:
                if trimmed.startswith("};") or trimmed == "}":
                    file_obj.structs.append(current_struct)
                    current_struct = None
                    continue

                if not trimmed.startswith("pub fn ") and not trimmed.startswith("fn "):
                    f_item = self._parse_field(trimmed, file_path, line_idx)
                    if f_item:
                        current_struct.fields.append(f_item)

            # Inside Union: Accumulate fields or close
            if current_union and not current_function:
                if trimmed.startswith("};") or trimmed == "}":
                    file_obj.unions.append(current_union)
                    current_union = None
                    continue

                if not trimmed.startswith("pub fn ") and not trimmed.startswith("fn "):
                    f_item = self._parse_field(trimmed, file_path, line_idx)
                    if f_item:
                        current_union.fields.append(f_item)

            # Function Start (using balanced parenthesis parsing)
            if not current_function:
                fn_match = self.FN_PREFIX_PATTERN.match(trimmed)
                if fn_match:
                    is_pub = bool(fn_match.group("pub"))
                    is_export = bool(fn_match.group("export"))
                    is_inline = bool(fn_match.group("inline"))
                    fn_name = fn_match.group("name")
                    rest = trimmed[fn_match.end():]

                    depth = 1
                    i = 0
                    while i < len(rest) and depth > 0:
                        if rest[i] == "(":
                            depth += 1
                        elif rest[i] == ")":
                            depth -= 1
                        i += 1

                    params_str = rest[:i-1] if i > 0 else ""
                    after_paren = rest[i:].strip()
                    ret_type = "void"
                    if after_paren:
                        ret_type = after_paren.rstrip("{;").strip() or "void"

                    params = self._parse_params(params_str)
                    is_generic = ret_type == "type" or any(p.is_comptime for p in params)

                    current_function = ZigFunction(
                        name=fn_name,
                        is_pub=is_pub,
                        is_export=is_export,
                        is_inline=is_inline,
                        is_generic=is_generic,
                        parameters=params,
                        return_type=ret_type,
                        location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                        raw_text=raw_line,
                    )
                    current_func_body = [raw_line]
                    brace_depth = raw_line.count("{") - raw_line.count("}")

                    # Single line function or semicolon decl
                    if (brace_depth <= 0 and "{" in raw_line) or (trimmed.endswith(";") and "{" not in raw_line):
                        current_function.body = "\n".join(current_func_body)
                        file_obj.functions.append(current_function)
                        if current_struct:
                            current_struct.methods.append(current_function)
                        current_function = None
                        current_func_body = []
                    continue

            # Accumulate Function Body
            if current_function:
                current_func_body.append(raw_line)
                brace_depth += raw_line.count("{") - raw_line.count("}")
                current_function.defers_count += len(re.findall(r"\bdefer\b", raw_line))
                current_function.errdefers_count += len(re.findall(r"\berrdefer\b", raw_line))
                current_function.tries_count += len(re.findall(r"\btry\b", raw_line))
                current_function.catches_count += len(re.findall(r"\bcatch\b", raw_line))
                current_function.switches_count += len(re.findall(r"\bswitch\s*\(", raw_line))
                current_function.branch_count += len(self.BRANCH_KEYWORDS.findall(raw_line))

                if "unreachable" in raw_line:
                    current_function.has_unreachable = True
                if "@panic" in raw_line:
                    current_function.has_panic = True
                if "@Vector" in raw_line:
                    current_function.has_simd = True
                if "asm volatile" in raw_line or "asm (" in raw_line:
                    current_function.has_inline_asm = True
                if "@ptrCast" in raw_line or "@alignCast" in raw_line:
                    current_function.has_ptrcast = True
                if "@typeInfo" in raw_line:
                    current_function.has_typeinfo = True

                if brace_depth <= 0:
                    current_function.body = "\n".join(current_func_body)
                    file_obj.functions.append(current_function)
                    if current_struct:
                        current_struct.methods.append(current_function)
                    current_function = None
                    current_func_body = []
                    brace_depth = 0

        # Flush if unclosed at EOF
        if current_struct:
            file_obj.structs.append(current_struct)
        if current_union:
            file_obj.unions.append(current_union)
        if current_function:
            current_function.body = "\n".join(current_func_body)
            file_obj.functions.append(current_function)

        return file_obj

    def parse_codebase(self, files: list[tuple[str, str]], target_path: str = "") -> CodeModel:
        model = CodeModel(target_path=target_path)
        for fpath, content in files:
            zig_file = self.parse_file(fpath, content)
            model.files.append(zig_file)
        return model
