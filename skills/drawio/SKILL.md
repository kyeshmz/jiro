---
name: drawio
description: Create, edit, export, and review draw.io diagrams in OpenCode. Use whenever the user asks to create, generate, draw, or design a diagram, flowchart, architecture diagram, ER diagram, sequence diagram, class diagram, network diagram, mockup, wireframe, or UI sketch, or mentions draw.io, drawio, .drawio files, or diagram export to PNG/SVG/PDF. Generates native .drawio XML with Mermaid or XML authoring, ELK auto-layout, and verified exports.
license: Apache-2.0
metadata:
  opencode/autoinvoke: false
---

# Draw.io Diagram Skill (OpenCode)

Generate draw.io diagrams as native `.drawio` files. Author each diagram as **Mermaid** (concise text that the draw.io desktop CLI converts and lays out for you) or as **draw.io XML** directly. Optionally auto-layout XML-authored diagrams with **ELK**, export to PNG/SVG/PDF with the diagram XML embedded, or generate a browser URL that opens the diagram directly in the draw.io editor.

OpenCode has no inline diagram viewer. This skill writes files, runs the desktop CLI when present, and prints absolute paths. If the open command fails, the printed path is the fallback.

## Authoring: Mermaid or XML?

The desktop CLI converts Mermaid to a native `.drawio` file and lays it out automatically, which is far more reliable than hand-positioning cells in XML.

| Author as | Best for | Needs desktop CLI? |
|-----------|----------|--------------------|
| **Mermaid** | Flowcharts, sequence, class, state, ER, gantt, mindmap, timeline, user journey, quadrant, C4, git graph, pie, and other standard types | Yes, to convert to `.drawio` |
| **XML** | Custom styling, precise positioning, specific shape libraries (AWS, Azure, network, UML detail), or when the desktop CLI is not installed | No (optional ELK layout needs the CLI) |

- Prefer Mermaid when the desktop CLI is available and the request is a standard type.
- Use XML for precise control or as the universal fallback. XML needs no CLI, so it is the only option when the desktop app is not installed.

Detect the CLI first (see Locating the CLI) if you are unsure it is present.

## The pipeline

Every diagram becomes a native `.drawio` file first, then is delivered in the requested output format.

1. **Author to `.drawio`**
   - **Mermaid**: write the Mermaid to a `.mmd` file, then convert:
     ```bash
     drawio -x -f xml -o diagram.drawio diagram.mmd
     ```
     Delete the `.mmd` afterward. The `.drawio` is the artifact.
   - **XML**: write the mxGraphModel XML to `diagram.drawio`, then run the repair pass. Optionally apply an ELK layout.
2. **Deliver**
   - *(no format)*: keep `diagram.drawio` and open it.
   - **png / svg / pdf**: export from the `.drawio` with embedded XML, then delete the source `.drawio`:
     ```bash
     drawio -x -f png -e -b 10 -o diagram.drawio.png diagram.drawio
     ```
   - **url**: build a browser URL from the XML, open it, and keep the `.drawio` as a local copy. See Browser URL output.
3. **Open the result.** Use the platform opener (`open` on macOS, `xdg-open` on Linux) or print the absolute path. If Mermaid was requested but no CLI is available, author the same diagram as XML.

Always convert Mermaid to `.drawio` first, then export. Direct Mermaid to PNG export with `-e` is broken in current draw.io Desktop (the embedded-XML step crashes). The two-step path is reliable and produces an editable embed.

## ELK layout for XML

The CLI `--layout` step auto-positions XML-authored diagrams with the editor's layout algorithms. Generate cells with approximate (or even `0,0`) positions and get the structure right. Use `verticalFlow` or `horizontalFlow` for flow-style diagrams and `organic` for networks. Mermaid-authored diagrams are already laid out. Do not add `--layout` to them.

Lay out in place after you write the file, or combine layout with export:

```bash
drawio -x -f xml --layout verticalFlow -o diagram.drawio diagram.drawio
drawio -x -f png -e -b 10 --layout verticalFlow -o diagram.drawio.png diagram.drawio
```

Presets: `verticalFlow` (top-to-bottom flows), `horizontalFlow` (left-to-right), `verticalTree`, `horizontalTree`, `radialTree`, `organic` (force-directed networks).

For finer control, pass a JSON array starting with `[` instead of a preset name:

```bash
drawio -x -f xml --layout '[{"layout":"elkLayered","config":{"elk.direction":"RIGHT"}}]' -o diagram.drawio diagram.drawio
```

Each entry is `{"layout": <algorithm>, "config": { ... }}`. Algorithms: `elkLayered`, `elkTree`, `elkRadial`, `elkOrganic`, `elkStress`, `elkBox`. Config keys starting with `elk.` are ELK options such as `elk.direction`, `elk.spacing.nodeNode`, and `elk.layered.spacing.nodeNodeBetweenLayers`. `edgeStyle` and `corners` control connector rendering.

Orthogonal edge routing without moving vertices:

```bash
drawio -x -f xml --layout libavoid -o diagram.drawio diagram.drawio
```

Run it on hand-positioned XML whose connectors cross shapes. Skip it after a flow or tree preset, which already routes edges.

## Mermaid syntax

Follow the bundled [Mermaid reference](references/mermaid-reference.md). It covers all supported diagram types plus flowchart styling (`style`, `classDef`, `linkStyle`). Match the language of the diagram labels to the user's language.

## Choosing the output format

Check the request for a format preference. Examples:

- "create a flowchart" → Mermaid → `flowchart.drawio`
- "png flowchart for login" → Mermaid → `login-flow.drawio.png`
- "svg: ER diagram" → Mermaid → `er-diagram.drawio.svg`
- "pdf AWS architecture overview" → XML (needs AWS shapes) → `architecture-overview.drawio.pdf`
- "url flowchart for user login" → opens browser at `app.diagrams.net`, keeps `login-flow.drawio` locally

If no format is mentioned, produce the `.drawio` file and open it.

PNG, SVG, and PDF are exported with `-e` (`--embed-diagram`). The file contains the full diagram XML, so opening it in draw.io recovers the editable diagram. Do not use `jpg`. It is lossy and cannot embed XML.

## Browser URL output

Keep the `.drawio` file on disk as the local copy, compress its XML with Node.js `zlib` into a `https://app.diagrams.net/#R...` URL, and open that in the browser. No draw.io Desktop is needed to view it.

Run this one-liner (replace `DIAGRAM.drawio` with the actual filename):

```bash
URL=$(node -e '
const fs = require("fs");
const zlib = require("zlib");
const xml = fs.readFileSync(process.argv[1], "utf8");
const compressed = zlib.deflateRawSync(encodeURIComponent(xml)).toString("base64");
console.log("https://app.diagrams.net/?grid=0&pv=0&border=10&edit=_blank#R" + encodeURIComponent(compressed));
' "DIAGRAM.drawio")
```

Do not use a `#create=` URL for XML. Draw.io rewrites that hash after loading, and when the rewrite differs from the link it asks "All changes will be lost!".

Open with `open "$URL"` on macOS or `xdg-open "$URL"` on Linux. Very large diagrams may exceed the browser URL length limit (roughly 32K to 2MB depending on the browser). Then open the `.drawio` file locally instead.

Print both handles:

```text
Opened in browser: <URL>
Local file: DIAGRAM.drawio
```

## draw.io CLI

The desktop app's CLI converts Mermaid to `.drawio`, applies ELK layouts (`--layout`), and exports to PNG/SVG/PDF. All three need the desktop app installed.

### Locating the CLI

Detect the environment first, then locate the CLI.

- **Linux (native)**: `drawio`, typically on PATH via snap, apt, or flatpak. Confirm with `which drawio`.
- **macOS**: this prints the first of `drawio` on PATH (Homebrew), `/Applications`, `~/Applications`, or Spotlight, or nothing if draw.io is absent:

```bash
{ command -v drawio; ls /Applications/draw.io.app/Contents/MacOS/draw.io ~/Applications/draw.io.app/Contents/MacOS/draw.io
  mdfind "kMDItemCFBundleIdentifier == 'com.jgraph.drawio.desktop'" | sed 's|$|/Contents/MacOS/draw.io|'; } 2>/dev/null | head -1
```

Call the binary inside the `.app`. A copy or symlink outside it dies with "Unable to find helper app".

Only once every step comes up empty should you treat the CLI as absent and fall back to XML authoring with `.drawio` or `url` output. Tell the user that installing the draw.io desktop app enables Mermaid conversion, layouts, and image export.

### Export command

```bash
drawio -x -f <format> -e -b 10 -o "<output>" "<input.drawio>"
```

Key flags:

- `-x` / `--export`: export mode (also used for Mermaid conversion and layouts)
- `-f` / `--format`: output format (`xml`, png, svg, pdf, jpg). Use `xml` to produce a `.drawio` from Mermaid or a layout
- `--layout`: run a layout before writing. An ELK preset name, `libavoid`, or a custom-layout JSON array
- `--mermaid-image 1`: convert Mermaid to a single static SVG image cell instead of an editable diagram. Only when the user explicitly asks for a non-editable image cell
- `-e` / `--embed-diagram`: embed diagram XML in the output (PNG, SVG, PDF only)
- `-o` / `--output`: output file path
- `-b` / `--border`: border width around diagram (default 0)
- `-t` / `--transparent`: transparent background (PNG only)
- `-s` / `--scale`: scale the diagram size
- `--width` / `--height`: fit into specified dimensions (preserves aspect ratio)
- `-a` / `--all-pages`: export all pages (PDF only)
- `-p` / `--page-index`: select a specific page (1-based)
- `--disable-gpu`: retry flag when a command dies with "GPU process isn't usable"

### Opening the result

| Environment | Command |
|-------------|---------|
| macOS | `open <file>` |
| Linux | `xdg-open <file>` |

If the opener fails, print the absolute path so the user can open it manually.

## File naming

- Use a descriptive, lowercase, hyphenated name based on the content (for example `login-flow`, `database-schema`).
- Exports use double extensions (`name.drawio.png`, `name.drawio.svg`, `name.drawio.pdf`) to signal embedded diagram XML.
- For `url` mode, keep the `.drawio` file (no double extension). The URL is a view and edit handle and the local file is the persistent copy.

## XML format

A `.drawio` file is native mxGraphModel XML, the same format the CLI converts Mermaid to.

Every diagram must have this structure:

```xml
<mxGraphModel adaptiveColors="auto">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
  </root>
</mxGraphModel>
```

- Cell `id="0"` is the root layer.
- Cell `id="1"` is the default parent layer.
- All diagram elements use `parent="1"` unless using multiple layers.
- Cells inside a container use `parent="<container_id>"` with coordinates relative to that container.
- Edges belong to the innermost container that holds both endpoints. Same container at any depth means that container's id. One end outside every container means `parent="1"`. An auto-layout reads edge coordinates in its parent frame, so an edge parked further out than its endpoints is laid out in the wrong place.

Never include XML comments in the output. Escape special characters in attribute values (`&amp;`, `&lt;`, `&gt;`, `&quot;`). Always use unique `id` values for each `mxCell`. Every edge needs a child `<mxGeometry relative="1" as="geometry" />`. A self-closing edge `mxCell` does not render.

### Repair pass

Run this right after writing XML to a `.drawio` file, before any layout, export, or URL step. It fixes text around the diagram (a code fence, a sentence, a stray closing tag), unescaped `<` or `&` inside an attribute value, and the default layer written as its own parent (`<mxCell id="1" parent="1"/>`, which hides everything). It changes nothing in a well-formed file and needs only Node.js. Skip it if `node` is not installed. Replace `DIAGRAM.drawio` with the actual filename:

```bash
node -e '
const fs = require("fs");
const file = process.argv[1];
let xml = fs.readFileSync(file, "utf8");
const diagram = xml.match(/<mxfile[\s\S]*?<\/mxfile>|<mxGraphModel[\s\S]*?<\/mxGraphModel>/);
if (diagram && xml.trim() !== diagram[0]) xml = diagram[0];
xml = xml.replace(/="([^"]*)"/g, function(m, v)
{
  return "=\"" + v.replace(/</g, "&lt;").replace(/&(?!(?:amp|lt|gt|quot|apos|#[0-9]+|#x[0-9a-fA-F]+);)/g, "&amp;") + "\"";
});
xml = xml.replace(/<mxCell id="([^"]+)" parent="\1"\s*\/>/g, "<mxCell id=\"$1\" parent=\"0\"/>");
fs.writeFileSync(file, xml);
' "DIAGRAM.drawio"
```

## XML reference

Follow the bundled essentials for most diagrams:

- [XML essentials](references/xml-essentials.md): skeleton, vertex and edge templates, labels, shapes, layout grid, containers, swimlanes, and edge styles.

Fetch the full reference only when a diagram needs layers, tags, metadata and placeholders, tables, cross-functional grids, or dark-mode colors. See [XML reference](references/xml-reference.md).

### Shapes and icons

When a diagram needs cloud, network, or brand icons (AWS, Azure, GCP, Cisco, Kubernetes, GitHub, Slack), never guess `mxgraph.*` names. Look them up with the bundled script (Node.js 18+, network), one query per icon narrowed by library (`aws4`, `azure2`, `cisco19`):

```bash
node <skill-folder>/scripts/find-shapes.js "aws4 lambda" "github" "slack"
```

It searches draw.io shape libraries, then its icon service, and prints `title width×height style` lines. Use a style as is.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| draw.io CLI not found | Desktop app not installed or not on PATH | Work through Locating the CLI. If absent, author as XML and deliver `.drawio` or `url`, and tell the user that installing the desktop app enables Mermaid conversion, layouts, and image export |
| Mermaid to PNG export crashes | Direct `.mmd` to PNG with `-e` is broken | Convert Mermaid to `.drawio` first (`-f xml`), then export the `.drawio` |
| Blank diagram from Mermaid | Misspelled type keyword or syntax error | Check the Mermaid reference. The first non-directive line's keyword selects the diagram type |
| Layout does nothing or errors | Unknown preset name, custom JSON not an array, or desktop build too old | Use a preset or a JSON array starting with `[`. On an old build, author as XML with explicit positions |
| Export produces empty or corrupt file | Invalid XML or missing root cells | Run the repair pass and check the basic structure |
| `GPU process isn't usable. Goodbye.` during convert, layout, or export | Electron cannot start a GPU process (VMs, CI, headless sessions) | Retry with `--disable-gpu` added |

## Provenance

Ported from the JGraph draw.io skill (`jgraph/drawio-mcp`, Apache-2.0). Upstream: `plugins/claude-code/skills/drawio/SKILL.md` plus `shared/mermaid-reference.md`, `shared/xml-essentials.md`, `shared/xml-reference.md`, and `scripts/find-shapes.js`. This OpenCode port removes WSL2, Windows-native, VS Code and Cursor opening paths, and MCP inline-viewer handling. Layout, authoring, repair, shapes, and licensing are unchanged. See `LICENSE`.
