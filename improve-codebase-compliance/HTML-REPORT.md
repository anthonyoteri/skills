# HTML Report Format

One self-contained HTML file in the OS temp directory, styled with Tailwind from its CDN. Static: no scripts beyond Tailwind.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Compliance review for {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="sources">...</section>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header and sources

Repo name, date, and totals (batches, sites, violations vs judgement calls). Then a compact table of standards sources: name, rule count, and a `Repo` or `Best practice` tag. When best practices were used, a prominent amber callout says the repo documents no standards and points at the standards-file candidate.

## Candidate card

One `<article>` per batch, in rank order:

- **Title**: names the change (e.g. "Replace bare `except:` with typed handlers").
- **Badge row**: rank, priority (`High` = red, `Medium` = amber, `Low` = slate), confidence (`Violation` or `Judgement call`), source tag (`Repo` or `Best practice`).
- **Rule**: the quoted rule and its source, in a muted blockquote.
- **Sites**: count, then a monospaced list of `path:line`, collapsed into a `<details>` past ten.
- **Before / After**: two code blocks side by side on one representative site. The centrepiece.
- **Why it matters**: one sentence.
- **Cost**: one sentence on effort and risk.
- **Enforce with** (if a check exists): the tool, the rule, and the config snippet that turns it on.
- **Exception callout** (if applicable): one line in an amber box citing the ADR or comment that may excuse it.

## Top recommendation

One larger card: the batch you'd tackle first, one sentence on why, an anchor link to its card.

## Style

Editorial, not dashboard: generous whitespace, one accent colour plus red and amber for priority. Bullets over paragraphs; if a card needs a paragraph, the before/after is doing too little.
