---
order: 4
---
# Mathematics

LaTeX-style notation, rendered locally with bundled KaTeX scripts and fonts.

## Inline equations

Write `$E = mc^2$` to produce $E = mc^2$. Markdown math is protected by the Arithmatex extension before rendering.

## Display equations

Use double dollar signs on separate lines:

```latex
$$
\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}
$$
```

$$
\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}
$$

## Aligned derivations

$$
\begin{aligned}
\nabla \cdot \mathbf{E} &= \frac{\rho}{\varepsilon_0} \\
\nabla \cdot \mathbf{B} &= 0 \\
\nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t}
\end{aligned}
$$

## Matrices

$$
A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix},
\qquad \det(A) = -2
$$

## Annotations and cases

$$
f(x) = \begin{cases}
x^2 & \text{if } x \geq 0 \\
-x & \text{otherwise}
\end{cases}
\qquad
\underbrace{a + \cdots + a}_{n\text{ terms}} = na
$$

!!! note "Math notation, not a full TeX distribution"
    KaTeX supports a substantial subset of LaTeX math. It does not compile complete `.tex` documents or load arbitrary LaTeX packages. Unsupported commands remain visible as errors instead of disappearing.

## Math inside code

Fenced examples and inline code stay literal: `$x^2$`. Only math marked by the Markdown extension is rendered.
