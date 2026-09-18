---
order: 1
---
# Documentation, without dependencies on the web.

A quiet place for your technical knowledge. Write in Markdown, explain with equations, and take everything with you.

<span class="pill">LOCAL BY DESIGN</span>

Welcome to **Fieldnotes**, a minimal MkDocs theme inspired by the familiar Read the Docs layout. A clear sidebar, comfortable typography, and room for the details that matter.

<div class="feature-grid" markdown="0">
<div class="feature"><strong>01 &nbsp; Truly self-contained</strong><p>Styles, scripts, math fonts, and search travel with your documentation.</p></div>
<div class="feature"><strong>02 &nbsp; Made for technical writing</strong><p>Readable code, LaTeX equations, tables, and helpful annotations.</p></div>
<div class="feature"><strong>03 &nbsp; Light or dark</strong><p>A considered palette for either setting. Choose with the theme button.</p></div>
<div class="feature"><strong>04 &nbsp; Your usual workflow</strong><p>Plain Markdown files, a local preview, and a portable HTML build.</p></div>
</div>

## Start with something simple

Create a page in `docs/`, add it to your navigation, and preview it locally:

```powershell
.\.venv\Scripts\python -m mkdocs serve
```

Changes appear in your browser as you save. No account, remote editor, or internet connection is required after setup.

!!! tip "Offline is the default"
    The generated site contains everything this theme needs. Copy the entire `site/` folder to another machine and open `index.html`.

## Code that reads clearly

Language-aware highlighting happens during the build, so reading your code needs no external service.

```python
from dataclasses import dataclass

@dataclass
class Experiment:
    name: str
    samples: list[float]

    def mean(self) -> float:
        return sum(self.samples) / len(self.samples)
```


## Give your ideas a little notation

Inline math such as $E = mc^2$ fits naturally into a sentence. Display equations get the space they need:

$$
\hat{\mu} = \frac{1}{N} \sum_{i=1}^{N} x_i
$$

## Explore the guide

| Need to… | Start here |
| --- | --- |
| Write your first page | [Getting started](guide/getting-started.md) |
| Highlight code and add notes | [Code & syntax](guide/code.md) |
| Typeset equations | [Mathematics](guide/math.md) |
| Prepare a disconnected machine | [Use this theme offline](offline.md) |
