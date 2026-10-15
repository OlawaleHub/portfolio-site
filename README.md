# Soliu Quadri — portfolio

A static, editorial-style portfolio site. No build step, no dependencies, no
package manager: open `index.html` and it works.

Design direction is modelled on the layout system used by
[treasureokure.com](https://treasureokure.com/) — paper ground, hairline rules,
a 12-column grid, small-caps labels with an accent bar, and a triple-accent
rotation across sections. All content is Soliu's own; nothing was copied from
the reference site.

---

## Running it locally

Open `index.html` directly in a browser. Everything is relative, so `file://`
works for the pages; a local server is only needed if you want the fetch-based
checks to run.

```powershell
# optional: serve it properly
& "C:\Users\USER\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" `
  -m http.server 8899 --directory .
```

Then visit <http://127.0.0.1:8899/>.

---

## Structure

```
portfolio-soliu/
├── index.html              Home — hero, about, record, selected work,
│                           services, skills, experience, working notes
├── about.html              Story, principles, record, experience, inventory
├── portfolio.html          Case-study index + all repositories + capabilities
├── notebook.html           Offline-first playbook, lessons, go-to sources
├── contact.html            Details, mailto form, links, FAQ
├── work/
│   ├── lagos-emergency.html
│   ├── ifeoluwa-medical.html
│   ├── token-gated-voting.html
│   ├── refcrypt-labs.html
│   ├── portfolio-builds.html
│   └── mobile-flutter.html
├── assets/
│   ├── css/site.css        The whole design system, one file
│   ├── js/site.js          Theme, drawer, tabs, reveal, form, year
│   └── img/
│       ├── profile-square.jpg  Square portrait (used by hero and About)
│       ├── profile-hero.jpg    Spare portrait crop, currently unreferenced
│       ├── og-card.jpg         1200×630 social card
│       ├── work/*.svg          Thumbnails for the home page
│       └── banners/*.svg       Wide case-study artwork
├── deploy-to-github.ps1    Commits, sets the remote and pushes to GitHub
├── vercel.json             Vercel config — clean URLs, no framework detection
├── DEPLOY.md               Step-by-step Vercel deployment guide
├── .gitattributes          LF normalisation; binary assets left alone
├── .gitignore / .vercelignore
└── _build/
    ├── build_cases.py          Generates the six work/*.html pages
    ├── verify_site.py          HTTP check: every page and local link
    ├── validate_structure.py   HTML structure, a11y and landmark checks
    └── make_banner.py          Regenerates the SVG artwork (see below)
```

---

## Design tokens

Everything is driven by custom properties at the top of `assets/css/site.css`.

| Token | Value | Used for |
| --- | --- | --- |
| `--green` / `--accent` | `#3f6b46` | Section bars, links, focus rings |
| `--carmine` / `--accent-alt` | `#8f0a30` | Links on hover, headnotes, arrows |
| `--ochre` / `--accent-third` | `#7a5e02` | Third section bar in the rotation |
| `--paper` | `#f0f0f0` | Page ground, with layered SVG grain |
| `--paper-sunk` | `#e3e3e3` | Row hover, table shading, inline code |
| `--ink` / `--ink-muted` | `#14130f` / `#6c6c6c` | Body text and secondary text |
| `--margin` | `2in` (1in ≤1200px, 1.25rem ≤900px) | Page gutter |
| `--cols` | `12` (6 ≤900px) | Grid columns |

Type: **Aboreto** for the big sign-off, **Figtree** for UI and headings,
**Newsreader** for body copy. Loaded from Google Fonts.

There is a dark theme on `:root[data-theme="dark"]`, toggled by the ☾ button and
remembered in `localStorage` under the key `sq-theme`. The inline script in each
`<head>` applies it before first paint so there is no flash.

---

## Images

Three portrait derivatives live in `assets/img/`, all cut from the original
`profile.jpg` (510×510) with its `#PHOTOLAB` watermark geometrically excluded —
nothing was painted over:

| File | Size | Used by |
| --- | --- | --- |
| `profile-square.jpg` | 510×510 | Home hero, About page |
| `profile-hero.jpg` | 510×382 | Spare; not currently referenced |
| `og-card.jpg` | 1200×630 | Social share card (`og:image`) |

**Why the hero uses the square one.** The `.portrait img` rule sets
`aspect-ratio: 3/4` with `object-fit: cover`, so any source is centre-cropped to
a 3:4 portrait. `profile-hero.jpg` is 510×382 — a 4:3 *landscape* — so feeding it
through a 3:4 frame would slice away roughly 63% of its width. The square file is
correctly framed on the face and crops symmetrically instead.

If you supply a genuine portrait-orientation photo, drop it in and set
`aspect-ratio` on `.portrait img` to match, or just leave the rule off.

**The real fix is a real photo.** The current portrait is a stylised illustration
from an avatar app, and the square is a 1.26× upscale of a 404×404 crop. A
straight-on photograph at portrait orientation would improve the hero more than
any CSS change.

---

## Editing the content

Most changes are plain HTML edits. Two things work differently:

**The six case studies are generated.** Edit the `PROJECTS` list in
`_build/build_cases.py`, then rebuild:

```powershell
& "C:\Users\USER\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" `
  _build\build_cases.py
```

Each project is a dictionary: `title`, `meta`, `tagline`, `accent`, `credits`,
`data` (the "At a glance" figures) and `body` (the numbered sections). Adding a
seventh project means adding a dictionary and updating the `/ 6` count in the
`SHELL` template.

**The artwork is generated.** `assets/img/work/*.svg` and
`assets/img/banners/*.svg` are abstract banners drawn from the accent palette.
They are placeholders for real screenshots — swap in a JPG or PNG of the same
aspect ratio (2:1 for thumbnails, 4:1 for banners) and update the `src`. The CSS
applies `filter: grayscale(1) contrast(1.04)` and `mix-blend-mode: multiply`, so
any replacement inherits the same editorial treatment automatically.

---

## Verifying after a change

Both scripts expect the site to be served on `127.0.0.1:8899`.

```powershell
$py = "C:\Users\USER\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
& $py _build\verify_site.py          # every page + every local link returns 200
& $py _build\validate_structure.py   # tags balanced, one h1, alt text, landmarks
```

`verify_site.py` reports the exact failing URL. `validate_structure.py` checks
duplicate ids, missing `alt` attributes, links with no accessible text, the
required landmarks on every page, and that every primary nav destination also
appears in the mobile drawer.

---

## Deploying

Full click-by-click instructions are in **[DEPLOY.md](DEPLOY.md)** — covering both
the Vercel drag-and-drop route and the GitHub import route that gives you
automatic redeploys.

The short version: drag the whole `portfolio-soliu` folder onto
<https://vercel.com/new>, leave the framework as **Other**, and deploy. There is
no build command and no output directory to configure.

`vercel.json` is committed and configures clean URLs (`/about` rather than
`/about.html`), disables framework detection so Vercel does not look for a
Next.js build, and adds long-lived caching for `/assets/**`. `.vercelignore`
keeps `_build/` and this documentation out of the published output.

All paths in the site are relative, so it also works unchanged on GitHub Pages
or Netlify.

---

## Content accuracy notes

These are deliberate and worth preserving when editing:

- **The statistics are real and countable.** "21 public repositories" is the
  actual count on GitHub. Nothing on this site uses invented outcome metrics —
  the previous version of the site showed animated counters that rendered as
  `0+`, because the real figures were never in the markup.- **There are no testimonials.** The previous version had none either. Rather
  than publish quotes nobody gave, the home page carries a "Working notes"
  section of first-person statements that are verifiable from the work.
- **The Capstone build caveats are stated on purpose.** The
  `token-gated-voting` page names two real defects in the committed contract
  (a four-argument `GovernorSettings` call and a Pausable import path that moved
  in OpenZeppelin 5.x). Fixing them means editing that page too.
- **The Lagos Emergency limitations are listed**, including the placeholder
  phone numbers and the unwired dispatch endpoint, because they are documented
  in the project's own README.
- **Refcrypt Labs' own site does not name Soliu.** The claim that he builds and
  maintains that platform comes from his portfolio, and the case study says the
  source is under NDA rather than implying it is public.
