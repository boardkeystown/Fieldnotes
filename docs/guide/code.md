---
order: 3
---
# Code & syntax

Clear examples, useful callouts, and structured reference material.

## Fenced code blocks

Put a language name after the opening triple backticks to enable build-time highlighting. The Copy button uses your browser clipboard, with a fallback for local files.

```python
from pathlib import Path

def read_notes(folder: Path) -> list[str]:
    """Read local Markdown documents."""
    return [path.read_text(encoding="utf-8")
            for path in folder.glob("*.md")]
```

```cpp
#include <iostream>

int main() {
    constexpr double speed = 299792458.0;
    std::cout << "Speed of light: " << speed << '\n';
}
```


```lua
function foobar() 

end
```


```yaml
theme:
  name: null
  custom_dir: theme
use_directory_urls: false
```

## Inline code

Use backticks for identifiers such as `read_notes()`, file names, or short commands.

## Annotations

!!! note "A useful detail"
    Notes provide context without interrupting the explanation.

!!! tip "Keep examples reproducible"
    Include inputs, expected output, and the assumptions behind the result.

!!! warning "Prepare before disconnecting"
    Python and the wheelhouse must be available on the destination machine before installation.

The Markdown for a note looks like this:

```markdown
!!! note "A useful detail"
    Indent the content with four spaces.
```

## Tables and footnotes

| Feature | Rendering | Network needed |
| --- | --- | --- |
| Code highlighting | Pygments at build time | No |
| Math | Bundled KaTeX | No |
| Search | Bundled page index | No |

Technical claims can include a footnote.[^example]

[^example]: Footnotes are part of the generated page and work offline too.
