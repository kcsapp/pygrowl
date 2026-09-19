"""
Parse the COMPAS "Program option list and default values" documentation page
(a reStructuredText file) into a list of dicts, one per non-deprecated
command-line option.

Each dict has the keys:
    "name"        : str            - the long option name, e.g. "--common-envelope-alpha"
    "short_name"  : str or None    - the short form, e.g. "-e" (None if there isn't one)
    "description" : str            - free-text description of the option
    "options"     : list[str]      - the set of valid string values for the option
                                      (empty list if the option doesn't take one of a
                                      fixed set of values, e.g. it's a float/int/string)
    "default"     : str or None    - the default value, as given in the docs (None if
                                      no "Default = ..." line was found)

Options whose entry contains a "DEPRECATION NOTICE:" are excluded, since they are
deprecated aliases that COMPAS intends to remove.

When emitting Python (`-t py`), generated fields are wrapped to respect a
configurable line length (`--line-length`, default 100), and any `Literal[...]`
type is always spelled out one member per line, e.g.:

    Literal[
        "value1",
        "value2",
    ]

Usage:
    python parse_compas_options.py [-o output.json]
"""

import argparse
import json
import re
import sys
import textwrap
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, NamedTuple

DOC_URL = (
    "https://raw.githubusercontent.com/TeamCOMPAS/COMPAS/refs/heads/dev/"
    "online-docs/pages/User%20guide/Program%20options/"
    "program-options-list-defaults.rst"
)

PY_SPACE = " " * 4

# Default max line length to respect when generating Python output. Overridable
# via the `--line-length` CLI flag.
DEFAULT_LINE_LENGTH = 100

PY_HEADER = """from typing import ClassVar, Literal

from growl.args import (
    AllowCompasRange,
    AllowCompasRangeOrSet,
    AllowCompasSet,
    AllowCompasVector,
    GrowlArgs,
    GrowlField,
    growl_transform,
)


@growl_transform
class CompasOptions(GrowlArgs):
    command: ClassVar[str] = "COMPAS"
"""

# Matches an option header line, e.g.:
#   **--eccentricity [ -e ]**
#   **--add-options-to-sysparms**
#   **--help [ -h ]**
HEADER_RE = re.compile(
    r"^\*\*(?P<flag>--[A-Za-z0-9][A-Za-z0-9\-]*)"
    r"(?:\s*\[\s*(?P<short>-[A-Za-z0-9])\s*\])?\s*\*\*",
    re.MULTILINE,
)

# Matches "Options: { A, B, C }" (possibly split across the rest of the line)
OPTIONS_RE = re.compile(r"Options:\s*\{([^}]*)\}")

# Matches "Default = ...", "Default: ...", or "Default shows ..." through to the
# end of that line (a couple of entries use "shows" instead of "=" or ":").
DEFAULT_RE = re.compile(r"Default\s*(?:[:=]|shows)\s*(.*)")

# Identify a float
FLOAT_RE = re.compile(r"^(\d+\.\d+)(?:\s*\\times\s*10\^\{?(\d+)\}?\s*)?")

# Backtick and non-ASCII quotation-mark characters that occasionally turn up in a
# scraped default value as stray doc-formatting artifacts (e.g. curly quotes from
# a smart-quotes pass) rather than being part of the actual value.
STRAY_QUOTE_CHARS_RE = re.compile("[`‘’“”„‚‹›«»]")


def clean_default_string(value: str) -> str:
    """Remove backtick and non-ASCII quotation-mark characters from a raw
    default-value string."""
    return STRAY_QUOTE_CHARS_RE.sub("", value)


# Sphinx/RST markup we want to strip out of free text so the description reads cleanly
INLINE_MARKUP_RES = [
    (re.compile(r"\|br\|"), " "),  # explicit line-break markup
    (re.compile(r":math:`([^`]*)`"), r"\1"),  # :math:`...` -> ...
    (re.compile(r":cite:`([^`]*)`"), r"[\1]"),  # :cite:`...` -> [...]
    (re.compile(r":doc:`([^`<]*)(<[^>]*>)?`"), r"\1"),  # :doc:`Text <target>` -> Text
    (re.compile(r"``([^`]*)``"), r"\1"),  # ``code`` -> code
    (re.compile(r"\*\*([^*]*)\*\*"), r"\1"),  # **bold** -> bold
]


@dataclass
class TypeAnnotation:
    """A minimal, structured representation of a (possibly generic/nested) type
    annotation, e.g. `float`, `Literal["a", "b"]`, or
    `AllowCompasSet[Literal["a", "b"]]`.

    Keeping this as a small tree - rather than a pre-formatted string - lets us
    defer formatting decisions (whether to break onto multiple lines, how far to
    indent) until we know the configured line length, and lets us guarantee that
    every `Literal[...]`, wherever it's nested, is always expanded one member per
    line rather than only when it happens not to fit.
    """

    head: str
    args: list["TypeAnnotation"] = field(default_factory=list)

    def contains_literal(self) -> bool:
        return self.head == "Literal" or any(a.contains_literal() for a in self.args)

    def render_inline(self) -> str:
        """Render as a single line, e.g. 'AllowCompasSet[Literal["a", "b"]]'."""
        if not self.args:
            return self.head
        return f"{self.head}[{', '.join(a.render_inline() for a in self.args)}]"

    def render(self, indent: str, line_length: int) -> str:
        """Render this annotation, assuming it starts at `indent`.

        Any subscript that contains a `Literal` is always broken one member per
        line (however deeply nested); other subscripts are only broken across
        multiple lines if their inline form would push the line past
        `line_length`.
        """
        if not self.args:
            return self.head

        inline = self.render_inline()
        if not self.contains_literal() and len(indent) + len(inline) <= line_length:
            return inline

        inner_indent = indent + PY_SPACE
        body = "\n".join(f"{inner_indent}{a.render(inner_indent, line_length)}," for a in self.args)
        return f"{self.head}[\n{body}\n{indent}]"


def fetch_text(url: str = DOC_URL) -> str:
    """Download the raw .rst file and return its text."""
    local_file = Path(url.split("/", -1)[-1])
    if local_file.exists():
        return local_file.read_text()

    req = urllib.request.Request(url, headers={"User-Agent": "compas-options-parser"})
    with urllib.request.urlopen(req) as resp:
        text = resp.read().decode("utf-8")
        local_file.write_text(text)
        return text


def clean_text(text: str) -> str:
    """Strip RST/Sphinx inline markup and collapse whitespace."""
    for pattern, repl in INLINE_MARKUP_RES:
        text = pattern.sub(repl, text)
    # Drop any remaining ref/directive-style tokens, e.g. ":ref:`Back to Top <...>`"
    text = re.sub(r":ref:`[^`]*`", "", text)
    # Collapse whitespace/newlines
    text = re.sub(r"[ \t]*\n[ \t]*", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_body_section(full_text: str) -> str:
    """
    Return only the portion of the document that contains individual option
    entries (i.e. the "COMPAS information" and "Alphabetical listing" sections),
    excluding the trailing "Category listing" section, which just lists option
    names without descriptions and would otherwise produce bogus/duplicate entries.
    """
    start_marker = "COMPAS information"
    end_marker = "Category listing"

    start = full_text.find(start_marker)
    end = full_text.find(end_marker, start if start != -1 else 0)

    if start == -1:
        start = 0
    if end == -1:
        end = len(full_text)

    return full_text[start:end]


def supports_vector(description: str) -> tuple[str, bool]:
    """Deduce whether an option is a Vector option from its description."""
    vector_option_text = " See Vector program options for option format."
    if description.endswith(vector_option_text):
        return description.removeprefix(vector_option_text), True
    else:
        return description, False


def supports_range(primitive_type: TypeAnnotation) -> bool:
    """Deduce whether an option supports Range values from its type annotation."""
    return not primitive_type.args and primitive_type.head in ("int", "float")


def supports_set(flag: str) -> bool:
    """Deduce whether an option supports Set values from its name."""
    lf = flag.lower()
    return not (
        lf == "--mode"
        or "output" in lf
        or "input" in lf
        or "file" in lf
        or "grid" in lf
        or "hdf5" in lf
        or "print" in lf
        or lf
        in (
            "--add-options-to-sysparams",
            "--log-level",
            "--yaml-template",
            "--quiet",
            "--debug-level",
        )
    )


def deduce_type_and_cast(
    flag: str, options: list[str], default: str | None
) -> tuple[TypeAnnotation, Any]:
    """Deduce the type of a field from its default, and handle some special cases.

    Using the live documentation is probably not as clear as doing something clever with the
    help text.
    """
    if default is None:
        if flag.startswith("--system-snapshot"):
            return TypeAnnotation("float"), None
        return TypeAnnotation("str | None"), None
    if m := FLOAT_RE.match(default):
        value, exponent = m.groups()
        fv = float(value)
        if exponent:
            fv *= 10 ** float(exponent)
        return TypeAnnotation("float"), fv
    if default.startswith("Random number"):
        return TypeAnnotation("float | None"), None
    if default.startswith("Current working directory"):
        return TypeAnnotation("str"), ""
    if "for each annotation" in default:
        return TypeAnnotation("str"), ""

    d = next((w for w in default.split() if w.strip()), default).strip(",")
    if d.lower() in ("true", "false"):
        return TypeAnnotation("bool"), d.lower() == "true"
    if options and d in options:
        literal = TypeAnnotation("Literal", [TypeAnnotation(f'"{v}"') for v in options])
        return literal, f'"{d}"'
    if d.isdigit():
        return TypeAnnotation("int"), int(d)

    d = clean_default_string(d)
    if not d or d == '""':
        return TypeAnnotation("str"), '""'

    return TypeAnnotation("str"), f'"{d}"'


class ParsedOption(NamedTuple):
    name: str
    flag: str
    short_name: str
    type_annotation: TypeAnnotation
    description: str
    options: list[str]
    default: Any


def parse_options(rst_text: str) -> list[ParsedOption]:
    """Parse the option entries out of the raw rst text, returning a list of dicts."""
    body = extract_body_section(rst_text)

    headers = list(HEADER_RE.finditer(body))
    results = []

    for i, match in enumerate(headers):
        block_start = match.end()
        block_end = headers[i + 1].start() if i + 1 < len(headers) else len(body)
        block = body[block_start:block_end]

        # Skip deprecated options entirely
        if "DEPRECATION NOTICE" in block:
            continue

        flag = match.group("flag").strip()
        short = match.group("short")

        # Skip --help and --version
        if flag in ("--help", "--version"):
            continue

        # Pull out "Options: { ... }" values, if present
        options_match = OPTIONS_RE.search(block)
        if options_match:
            options_list = [opt.strip() for opt in options_match.group(1).split(",") if opt.strip()]
        else:
            options_list = []

        # Pull out "Default = ..." value, if present. Only take the rest of that
        # single line (defaults are always given on one line in this doc).
        default_match = DEFAULT_RE.search(block)
        default_value = None
        if default_match:
            default_line = default_match.group(1)
            # Cut off at the next "|br|" or newline, whichever comes first
            default_line = re.split(r"\|br\|", default_line)[0]
            default_line = default_line.split("\n")[0]
            default_value = clean_text(default_line).rstrip(" |")
            default_value = default_value.strip()

        # Description = everything in the block up to the first "Options:" or
        # "Default" marker, or up to any RST directive block (list-table, etc.)
        desc_end_candidates = []
        for marker_re in (
            OPTIONS_RE,
            DEFAULT_RE,
            re.compile(r"\n\s*\n"),  # blank line -> end of first paragraph
            re.compile(r"\n\.\. "),  # start of an RST directive (list-table, comment, etc.)
        ):
            m = marker_re.search(block)
            if m:
                desc_end_candidates.append(m.start())
        desc_end = min(desc_end_candidates) if desc_end_candidates else len(block)
        description = clean_text(block[:desc_end])

        # Deduce a type annotation and cast default to that type
        primitive_type, default_value = deduce_type_and_cast(flag, options_list, default_value)
        description, use_vector = supports_vector(description)
        if use_vector:
            type_annotation = TypeAnnotation("AllowCompasVector", [primitive_type])
        else:
            wrapper_names = []
            if supports_range(primitive_type):
                wrapper_names.append("Range")
            if supports_set(flag):
                wrapper_names.append("Set")

            if wrapper_names:
                type_annotation = TypeAnnotation(
                    f"AllowCompas{'Or'.join(wrapper_names)}", [primitive_type]
                )
            else:
                type_annotation = primitive_type

        # convert flag name to option name
        name = flag.strip("-").replace("-", "_").lower()

        results.append(
            ParsedOption(
                name=name,
                flag=flag,
                type_annotation=type_annotation,
                short_name=short,
                description=description,
                options=options_list,
                default=default_value,
            )
        )

    # Some options are documented twice - keep the more complete (later) entry
    deduped = {}
    for entry in results:
        deduped[entry.name] = entry
    return list(deduped.values())


def output_as_json(options: list[ParsedOption], output: str | None):
    dicts = []
    for option in options:
        d = option._asdict()
        d["type_annotation"] = option.type_annotation.render_inline()
        dicts.append(d)

    text = json.dumps(dicts, indent=2)
    if output:
        with open(output, "w") as f:
            f.write(text)
        print(f"Wrote {len(options)} options to {output}", file=sys.stderr)
    else:
        print(text)


def render_field_signature(
    name: str, type_annotation: TypeAnnotation, indent: str, line_length: int
) -> str:
    """Render the `name: Type = GrowlField(` opening of one field.

    The type is kept inline if it fits within `line_length` and doesn't contain
    a `Literal` (which is always expanded, regardless of length); otherwise it's
    broken across multiple lines via `TypeAnnotation.render`.
    """
    suffix = " = GrowlField("
    inline_line = f"{indent}{name}: {type_annotation.render_inline()}{suffix}"
    if not type_annotation.contains_literal() and len(inline_line) <= line_length:
        return inline_line

    rendered_type = type_annotation.render(indent, line_length)
    return f"{indent}{name}: {rendered_type}{suffix}"


def _wrap_string_kwarg(
    key: str,
    quoted_body: str,
    prefix: str,
    indent: str,
    line_length: int,
    *,
    break_on_hyphens: bool = True,
    drop_whitespace: bool = True,
) -> str:
    """Render `key=<prefix>"<quoted_body>",` at `indent`, splitting the string
    literal into several adjacent (auto-concatenated) literals if it would
    otherwise exceed `line_length`.
    """
    single_line = f'{indent}{key}={prefix}"{quoted_body}",'
    if len(single_line) <= line_length:
        return single_line

    inner_indent = indent + PY_SPACE
    available = max(line_length - len(inner_indent) - len(prefix) - 2, 20)  # 2 = quote chars
    chunks = textwrap.wrap(
        quoted_body,
        width=available,
        break_on_hyphens=break_on_hyphens,
        drop_whitespace=drop_whitespace,
    ) or [""]
    body = "\n".join(f'{inner_indent}{prefix}"{chunk}"' for chunk in chunks)
    return f"{indent}{key}=(\n{body}\n{indent}),"


def format_description_kwarg(description: str, indent: str, line_length: int) -> str:
    escaped = description.replace('"', r"\"")
    # Never break on a hyphen (a split "well" + "-known" -> "well-\nknown" would
    # silently change the text), and keep any trailing space a wrapped line
    # naturally ends with, since dropping it would glue two words together once
    # the adjacent string literals are concatenated back into one string.
    return _wrap_string_kwarg(
        "description",
        escaped,
        "r",
        indent,
        line_length,
        break_on_hyphens=False,
        drop_whitespace=False,
    )


def format_default_kwarg(default: Any, indent: str, line_length: int) -> str:
    line = f"{indent}default={default!s},"
    if len(line) <= line_length:
        return line

    # `default` is only ever a number, bool, or a short quoted string in
    # practice, so this is a defensive fallback rather than something expected
    # to trigger often; wrap it the same way as `description` when it's a
    # quoted string, otherwise just leave the (already short) literal as-is.
    body = str(default)
    if body.startswith('"') and body.endswith('"'):
        return _wrap_string_kwarg("default", body[1:-1], "", indent, line_length)
    return line


def build_field(option: ParsedOption, line_length: int) -> str:
    """Render one `GrowlField(...)` class attribute, respecting `line_length`."""
    name_indent = PY_SPACE
    body_indent = PY_SPACE * 2

    signature = render_field_signature(
        option.name, option.type_annotation, name_indent, line_length
    )

    kwarg_lines = [
        format_description_kwarg(option.description, body_indent, line_length),
        format_default_kwarg(option.default, body_indent, line_length),
    ]
    if any(c.isupper() for c in option.flag):
        kwarg_lines.append(f'{body_indent}flag="{option.flag}",')

    body = "\n".join(kwarg_lines)
    return f"{signature}\n{body}\n{PY_SPACE})"


def output_as_python(
    options: list[ParsedOption], output: str | None, line_length: int = DEFAULT_LINE_LENGTH
):
    segments = [PY_HEADER]
    for option in options:
        segments.append(build_field(option, line_length))

    text = "\n".join(segments) + "\n"
    if output:
        with open(output, "w") as f:
            f.write(text)
        print(f"Wrote {len(options)} fields to CompasOptions in {output}", file=sys.stderr)
    else:
        print(text)


def main():
    parser = argparse.ArgumentParser(description="Parse COMPAS program options docs.")
    parser.add_argument(
        "-f",
        "--output-file",
        default="src/growl/config.py",
        help="Path to write output (default: src/growl/config.py)",
    )
    parser.add_argument(
        "-t",
        "--output-type",
        default="py",
        choices=["json", "py"],
        help="Output format to write; JSON or a python file containing the class `CompasOptions`",
    )
    parser.add_argument(
        "-l",
        "--line-length",
        type=int,
        default=DEFAULT_LINE_LENGTH,
        help=f"Max line length in generated Python output (default: {DEFAULT_LINE_LENGTH})",
    )
    parser.add_argument(
        "--url", default=DOC_URL, help="Override the URL of the .rst source document"
    )
    args = parser.parse_args()

    raw_text = fetch_text(args.url)
    options = parse_options(raw_text)

    if args.output_type == "json":
        output_as_json(options, args.output_file)
    elif args.output_type == "py":
        output_as_python(options, args.output_file, args.line_length)


if __name__ == "__main__":
    main()
