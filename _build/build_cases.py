"""Build the six case-study pages from one template.

Each project is data; the shell markup lives in TEMPLATE. Run with the bundled
Python: it writes work/*.html next to the other site files.
"""
import html
import os
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent if "__file__" in globals() else pathlib.Path.cwd()
OUT = ROOT / "work"
OUT.mkdir(parents=True, exist_ok=True)

PAPER = "#f0f0f0"
ACCENT = {"green": "#3f6b46", "carmine": "#8f0a30", "ochre": "#7a5e02", "ink": "#14130f"}


def banner_svg(a: str, b: str, w: int = 1600, h: int = 400) -> str:
    """Abstract editorial banner, returned as a data URI so it can be filtered."""
    svg = f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}'>
<defs><pattern id='d' width='22' height='22' patternUnits='userSpaceOnUse'><circle cx='4' cy='4' r='1.2' fill='#14130f' opacity='0.5'/></pattern></defs>
<rect width='{w}' height='{h}' fill='{PAPER}'/>
<rect width='{w}' height='{h}' fill='url(%23d)'/>
<circle cx='{int(w*0.8)}' cy='70' r='190' fill='{a}' opacity='0.16'/>
<circle cx='{int(w*0.15)}' cy='340' r='220' fill='{b}' opacity='0.13'/>
<path d='M0 320 L{w} 120' stroke='{a}' stroke-width='2' opacity='0.45'/>
<path d='M0 360 L{w} 160' stroke='{b}' stroke-width='1' opacity='0.38'/>
<path d='M{int(w*0.56)} {h} L{int(w*0.68)} 0' stroke='{a}' stroke-width='1' opacity='0.30'/>
<path d='M{int(w*0.74)} {h} L{int(w*0.85)} 0' stroke='{b}' stroke-width='1' opacity='0.28'/>
<rect x='{int(w*0.84)}' y='240' width='150' height='150' fill='none' stroke='#14130f' stroke-width='1.5' opacity='0.4'/>
<circle cx='120' cy='80' r='40' fill='none' stroke='{b}' stroke-width='1.5' opacity='0.55'/>
<circle cx='120' cy='80' r='18' fill='{a}' opacity='0.32'/>
<g stroke='#14130f' stroke-width='1' opacity='0.22'>
<line x1='{int(w*0.25)}' y1='0' x2='{int(w*0.25)}' y2='{h}'/>
<line x1='{int(w*0.5)}' y1='0' x2='{int(w*0.5)}' y2='{h}'/>
<line x1='{int(w*0.75)}' y1='0' x2='{int(w*0.75)}' y2='{h}'/>
</g>
<rect x='0' y='0' width='{w}' height='6' fill='{a}' opacity='0.85'/>
</svg>"""
    return "data:image/svg+xml;utf8," + svg.replace("\n", "").replace("#", "%23")


# ---------------------------------------------------------------- shell

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Soliu Quadri</title>
<meta name="description" content="{meta}">
<meta name="author" content="Soliu Olawale Quadri">
<meta name="theme-color" content="#f0f0f0">
<meta property="og:title" content="{title} — Soliu Quadri">
<meta property="og:description" content="{meta}">
<meta property="og:type" content="article">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' fill='%2314130f'/%3E%3Ctext x='50' y='68' font-family='Georgia,serif' font-size='54' fill='%23f0f0f0' text-anchor='middle'%3ESQ%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Aboreto&family=Figtree:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap">
<link rel="stylesheet" href="../assets/css/site.css">
<script>
(function(){{try{{var t=localStorage.getItem("sq-theme");if(t==="dark"||(!t&&window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches)){{document.documentElement.setAttribute("data-theme","dark");}}}}catch(e){{}}}})();
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<div class="shell">
  <header class="masthead-bar">
    <div class="page">
      <div class="bar">
        <a href="../index.html" class="wordmark">Soliu Quadri<span>.</span></a>
        <nav class="nav" aria-label="Primary">
          <a href="../about.html" class="nav-item">About</a>
          <a href="../portfolio.html" class="nav-item">Portfolio</a>
          <a href="../notebook.html" class="nav-item">Notebook</a>
          <a href="../contact.html" class="nav-item">Contact</a>
        </nav>
        <button type="button" class="theme-toggle" aria-label="Switch to dark mode" title="Switch to dark mode"><span aria-hidden="true">&#9789;</span></button>
        <button class="burger" aria-expanded="false" aria-controls="drawer">
          <span class="sr-only">Open menu</span>
          <span class="bar-line" aria-hidden="true"></span>
          <span class="bar-line" aria-hidden="true"></span>
        </button>
      </div>
    </div>
  </header>

  <div id="drawer" class="drawer" inert aria-hidden="true">
    <div class="page">
      <a href="../index.html" class="drawer-link">Home</a>
      <a href="../about.html" class="drawer-link">About</a>
      <a href="../portfolio.html" class="drawer-link">Portfolio</a>
      <a href="../notebook.html" class="drawer-link">Notebook</a>
      <a href="../contact.html" class="drawer-link">Contact</a>
    </div>
  </div>

  <main id="main">
    <div class="page">
      <section class="case-head">
        <div class="folio">
          <a href="../portfolio.html" class="label label-ink folio-link">&larr; Index</a>
          <span class="label">Case study {index} / 6</span>
          <a href="{next_file}" class="label label-accent folio-link">{folio_next} &rarr;</a>
        </div>

        <figure class="banner">
          <img src="{banner}" alt="{banner_alt}" width="1600" height="400">
        </figure>

        <h1 class="display case-title">
{title_lines}
        </h1>
        <p class="lead case-tagline">{tagline}</p>

        <dl class="credits">
{credits}
        </dl>
      </section>

      <section class="glance">
        <p class="label glance-label">At a glance</p>
        <div class="data">
{data_rows}
        </div>
      </section>

{body}

      <nav class="case-foot" aria-label="Case study navigation">
        <a href="../portfolio.html" class="foot-side label label-ink">&larr; Back to index</a>
        <a href="{next_file}" class="foot-next">
          <span class="label">Next case study</span>
          <span class="foot-next-name">{next_title} <span aria-hidden="true">&rarr;</span></span>
        </a>
      </nav>
    </div>
  </main>

  <footer class="colophon">
    <div class="page">
      <p class="signoff">Soliu Quadri</p>
      <div class="grid mt-8">
        <div class="c-4">
          <p class="label">Soliu Quadri</p>
          <p class="colophon-note">Software engineer &mdash; web &amp; mobile. Lagos, Nigeria.</p>
          <p class="colophon-note">&copy; <span data-year>2026</span></p>
        </div>
        <div class="c-4">
          <p class="label">Contact</p>
          <ul class="colophon-list">
            <li><a class="link" href="mailto:quadrisoliu14@gmail.com">quadrisoliu14@gmail.com</a></li>
            <li><a class="link" href="tel:+2347054355120">+234 705 435 5120</a></li>
          </ul>
        </div>
        <div class="c-4">
          <p class="label">Elsewhere</p>
          <ul class="colophon-list">
            <li><a class="link" href="https://github.com/OlawaleHub" target="_blank" rel="noopener">GitHub</a></li>
            <li><a class="link" href="https://www.linkedin.com/in/quadri-soliu-9448bb1a6" target="_blank" rel="noopener">LinkedIn</a></li>
            <li><a class="link" href="https://twitter.com/Sulphate04" target="_blank" rel="noopener">X / Twitter</a></li>
          </ul>
        </div>
      </div>
    </div>
  </footer>
</div>

<script src="../assets/js/site.js" defer></script>
</body>
</html>
"""

# ---------------------------------------------------------------- projects

PROJECTS = [
    {
        "file": "lagos-emergency.html",
        "title": "Lagos Emergency",
        "meta": "A one-tap, offline-first emergency reporting PWA for Lagos. Next.js, IndexedDB, service workers and background sync.",
        "tagline": "Three buttons, no internet required, and a fallback for every point of failure.",
        "accent": ("carmine", "green"),
        "title_lines": "          <span>Lagos</span>\n          <span>Emergency</span>",
        "banner_alt": "Abstract artwork in carmine and green representing the Lagos Emergency project",
        "credits": [
            ("Role", "Front-end engineering &amp; offline architecture"),
            ("Scope", "Product design · PWA · Offline storage · Geolocation · Map integration"),
            ("Stack", "Next.js 14 · React 18 · Tailwind CSS · Service Worker · IndexedDB · Background Sync · Leaflet &amp; OpenStreetMap · lucide-react"),
            ("Links", '<a class="link" href="https://lagos-emergency-pwa.vercel.app/" target="_blank" rel="noopener">Live app &#8599;</a> &nbsp;·&nbsp; <a class="link" href="https://github.com/OlawaleHub/lagos-emergency-pwa" target="_blank" rel="noopener">Source &#8599;</a>'),
        ],
        "data": [
            ("Zero", "Internet required to accept an emergency report"),
            ("3", "Colour-coded buttons — Police, Fire, Medical"),
            ("20", "Lagos LGAs available for manual fallback routing"),
            ("2", "Sync paths — Background Sync plus an online-event replay"),
            ("8", "Priority features tracked and delivered"),
            ("112 / 767", "Direct-dial numbers surfaced for life-threatening cases"),
        ],
        "body": [
            (1, "The brief", """<p>Lagos is a city of roughly twenty million people and a road network that does not forgive hesitation. If you need an ambulance, the sequence is usually: find your phone, work out which number to call, hope you can describe where you are, and hope somebody on the other end can act on that description.</p>
<p>The premise of this project was narrow on purpose: reduce that sequence to a single tap. Not a directory of emergency services, not a form, not an account. One screen, three buttons, and the app works out the rest.</p>
<p>It was built under the <a href="https://refcryptlabs.com/" target="_blank" rel="noopener">Refcrypt Labs</a> banner as a public-good project rather than a commercial one, and it is live and installable today.</p>"""),
            (2, "Why offline-first was non-negotiable", """<p>Every emergency product has the same uncomfortable property: it is needed most at the exact moment the infrastructure around it is failing. Network congestion, a downed mast, a building with no signal — the scenarios where you need help are frequently the scenarios where you have no connection.</p>
<p>So the app assumes from the first line of code that the request will not reach a server. Tapping a button writes the alert to an <strong>IndexedDB queue</strong> and confirms immediately. The user sees that something happened. Synchronisation then becomes a background problem instead of a blocker.</p>
<p>The app shell itself is precached by a service worker, so the interface loads with no network at all — there is a dedicated offline fallback route rather than the browser's dinosaur.</p>"""),
            (3, "How the queue actually works", """<p>Two mechanisms drain the queue, because browser support is not uniform:</p>
<ul>
<li><strong>Background Sync</strong> — the service worker listens for the <code>sync</code> event and replays queued alerts when the browser decides the connection is usable again.</li>
<li><strong>The <code>online</code> event</strong> — a client-side listener does the same replay as a fallback for browsers without Background Sync support.</li>
</ul>
<p>There is a <code>/queue</code> screen where the user can see exactly what is pending and trigger a manual sync, and an <code>/offline</code> shell so the app degrades visibly rather than silently.</p>
<p>The test I insist on: turn the network off properly — not throttled, off — tap a button, confirm the alert appears in the queue, then restore the connection and watch the queue drain. If you have not watched it empty, you have not tested it.</p>"""),
            (4, "Routing when the sensor says no", """<p>Geolocation is a permission prompt, and permission prompts get denied. On tap the app requests the current position with a timeout; if the user refuses, or the fix fails, or the API is unavailable, the app does not stop.</p>
<p>It falls back to a dropdown of all <strong>twenty Lagos local government areas</strong>. Choosing one resolves the nearest police, fire and medical facilities for that area by distance, using haversine calculations against a local facility list — no API key, no server round trip, which matters precisely because the network is the thing that failed.</p>
<p>Facilities can also be found proactively on the <code>/locate</code> screen, which plots them on a Leaflet map with OpenStreetMap tiles. There is a reason that screen exists outside an emergency: nobody wants to discover a product's flaws while panicking.</p>"""),
            (5, "Accessibility and the small screens", """<p>The entire flow is designed for one-handed use under stress. Buttons are large, colour-coded and labelled with text as well as colour, so the distinction does not depend on colour vision. The home screen is a single screen — there is no scroll and no navigation required to act.</p>
<p>The app is installable as a PWA with a manifest and icons, so it can live on the home screen next to the phone dialler rather than behind a browser and three taps.</p>"""),
            (6, "What I would do differently", """<p>This project ships with documented gaps, and I would rather list them than let them be discovered:</p>
<ul>
<li><strong>The phone numbers in the constants file are placeholders.</strong> They need replacing with verified lines from each agency before this should be relied on. That is the single most important outstanding item.</li>
<li><strong>The facility list should expand to all twenty LGAs.</strong> Coverage is uneven and routing quality depends directly on it.</li>
<li><strong>The dispatch endpoint acknowledges and logs.</strong> <code>POST /api/emergency</code> currently accepts an alert and records it; wiring it to a real dispatch system — an agency API or an SMS gateway — is what turns this from a demonstration into infrastructure.</li>
<li><strong>iOS needs a 180&times;180 touch icon</strong> before it installs cleanly on an iPhone.</li>
</ul>
<p>The broader lesson I took from building it is about ambiguity in offline queues. A write can succeed on the server and fail on the way back, leaving the client unsure whether to retry. For an alert that triggers a dispatch, retrying twice could send two responders and not retrying could send none. No library resolves that for you — it is a product decision about which failure is worse, and it belongs written down rather than hidden in a callback.</p>
<p>What I am proudest of is not the technical machinery. It is that the response to &ldquo;how do I get help&rdquo; became a single tap.</p>"""),
        ],
    },
    {
        "file": "ifeoluwa-medical.html",
        "title": "Ifeoluwa Medical",
        "meta": "A no-code medical publishing platform built with Next.js App Router and Sanity CMS, with 60-second ISR revalidation.",
        "tagline": "A publishing platform where a doctor writes and publishes without ever calling a developer.",
        "accent": ("green", "ink"),
        "title_lines": "          <span>Ifeoluwa</span>\n          <span>Medical</span>\n          <span>Articles</span>",
        "banner_alt": "Abstract artwork in green and ink representing the Ifeoluwa Medical publishing platform",
        "credits": [
            ("Role", "Full-stack build — architecture, CMS modelling, front end"),
            ("Scope", "Headless CMS · Content modelling · Server rendering · ISR · Accessibility"),
            ("Stack", "Next.js 14 App Router · Sanity 3 · next-sanity · Portable Text · Tailwind CSS · next/image · lucide-react"),
            ("Links", '<a class="link" href="https://ifeoluwa-medical-czhv.vercel.app/" target="_blank" rel="noopener">Live site &#8599;</a> &nbsp;·&nbsp; <a class="link" href="https://github.com/OlawaleHub/ifeoluwa-medical" target="_blank" rel="noopener">Source &#8599;</a>'),
        ],
        "data": [
            ("0", "Lines of code the author needs to touch to publish"),
            ("60s", "Revalidation window before a new article appears"),
            ("5", "Surface routes — home, index, article, about, studio"),
            ("Static", "Delivery model for every public page"),
            ("1", "Embedded Studio at /studio for writing"),
            ("3", "Layers of content modelling — article, author, image"),
        ],
        "body": [
            (1, "The brief", """<p>A medical professional wanted to publish health writing for the general public — practical, evidence-based, and deliberately free of the two failure modes that dominate health content online: impenetrable jargon and fear-mongering.</p>
<p>The requirement that shaped every technical decision was not visual. It was ownership. She needed to be able to write and publish on her own schedule without opening a code editor, and without a developer in the loop for routine updates.</p>
<p>The site carries a standing disclaimer on every page — that the content is informational and not medical advice — which is a content-governance decision as much as a legal one.</p>"""),
            (2, "Choosing a headless CMS over a database", """<p>The obvious alternative was a conventional database with a small admin panel. I chose a headless CMS instead, and the deciding factor was what the author would actually experience.</p>
<p>Sanity gives a purpose-built editing environment for rich text and images out of the box, with a preview of structured content rather than a pile of HTML. Building an equivalent editor by hand would have taken longer and been worse.</p>
<p>The content model is deliberately small: an <strong>article</strong> with rich text, a cover image and an author reference; an <strong>author</strong> record; and Sanity's image pipeline for assets. Small models are easier for editors to reason about, and they do not accumulate dead fields.</p>"""),
            (3, "The Studio lives inside the site", """<p>The single most useful decision was embedding <strong>Sanity Studio at <code>/studio</code></strong> rather than hosting it separately. The author logs in on the same domain as the public site and gets the full editing interface there.</p>
<p>That removes an entire class of confusion. There is one URL to remember, one login, and no separation between &ldquo;the website&rdquo; and &ldquo;the thing I write in&rdquo;. From her side, writing an article is a form on a page she recognises.</p>"""),
            (4, "Static pages, live content", """<p>Public pages are statically generated, which is what makes the site fast on a phone over a poor connection. The tension with static generation is freshness: how does a newly published article appear without a redeploy?</p>
<p>The answer is incremental static regeneration with a <strong>60-second revalidation window</strong>. An article publishes in the Studio, and within a minute the public pages have rebuilt in the background. Readers get static-delivery speed; the author gets near-live publishing. Nobody has to trigger a deploy.</p>"""),
            (5, "Details worth naming", """<ul>
<li><strong>Images</strong> are served through <code>next/image</code> from Sanity's CDN, with the remote pattern allow-listed in the Next config, so covers are resized and served in modern formats automatically.</li>
<li><strong>Rich text</strong> renders through Portable Text, which means the published markup stays semantic rather than inheriting whatever the editor pasted in.</li>
<li><strong>Article count</strong> on the about page is derived from the content itself, not hand-maintained, so it cannot drift out of date.</li>
<li><strong>Typography and layout</strong> are kept deliberately plain: a medical-blue and white palette, comfortable measure, and no decorative elements competing with the writing.</li>
</ul>"""),
            (6, "What I would do differently", """<p>The honest limitation is volume: the site was built and handed over with a single published article, so it has been proven as a working platform but not yet stress-tested against a large back catalogue. Pagination on the article index, related-article logic, and search are the three things I would build next, and all three only meaningfully matter once there are dozens of posts rather than one.</p>
<p>I would also add structured data and an RSS feed from the start. Health writing is exactly the kind of content that benefits from being discoverable outside the site it lives on, and both are cheap to add early and annoying to retrofit.</p>
<p>What the project did prove is the part that mattered to the client: she can publish on her own, immediately, and the site stays fast.</p>"""),
        ],
    },
    {
        "file": "token-gated-voting.html",
        "title": "Token-Gated Voting",
        "meta": "A decentralised governance platform on Ethereum with paid voting, automatic refunds and a 4% quorum, built on OpenZeppelin Governor.",
        "tagline": "Governance where influence costs something, and cancelling a vote gives the money back.",
        "accent": ("ochre", "carmine"),
        "title_lines": "          <span>Token-Gated</span>\n          <span>Voting</span>",
        "banner_alt": "Abstract artwork in ochre and carmine representing the token-gated voting contracts",
        "credits": [
            ("Role", "Smart contract engineering (group capstone, four authors)"),
            ("Scope", "Solidity contracts · Governance extension · Test suite · Deployment scripts"),
            ("Stack", "Solidity · OpenZeppelin Governor · Hardhat · TypeScript · ethers v6 · TypeChain · ERC-20 &amp; ERC20Votes"),
            ("Links", '<a class="link" href="https://github.com/OlawaleHub/token-gated-voting" target="_blank" rel="noopener">Source &#8599;</a>'),
        ],
        "data": [
            ("4%", "Quorum, as a fraction of past total supply"),
            ("10 VOTE", "Example cost to cast a single vote"),
            ("1", "Vote per address per proposal, enforced"),
            ("8", "OpenZeppelin modules composed into the governor"),
            ("2", "Refund paths — cancelled proposals and treasury or burn"),
            ("Snapshot", "Vote weight taken from a past block, not the current one"),
        ],
        "body": [
            (1, "The brief", """<p>Most token governance has a participation problem that is easier to see than to solve. Holding a token is free, so voting costs nothing, so the people who show up are the ones with the strongest opinion rather than the strongest stake — and a determined actor can borrow a large position, vote, and return it in the same transaction.</p>
<p>The premise of this capstone was to make influence cost something. A voter pays a fixed amount of an ERC-20 token to cast a vote, and gets it back if the proposal is cancelled. Economic alignment, rather than pure token weighting.</p>
<p>It was built as a four-person group capstone over the WEB3 programme, and I wrote the governor extension and its test suite.</p>"""),
            (2, "Building on Governor rather than from scratch", """<p>Governance is a domain where inventing your own mechanics is a bad instinct. Vote counting, proposal lifecycle, timelocks and quorum all have well-understood failure modes that a battle-tested implementation has already met.</p>
<p>So the contract extends <strong>OpenZeppelin's Governor</strong>, composing the modules it needs: proposal settings, simple counting, token voting, quorum as a fraction of supply, timelock control, role-based access control and a pause switch. That is eight modules assembled into one governor rather than a bespoke voting contract.</p>
<p>The custom behaviour sits on top as <code>PaidGovernor</code>: the payment, the refund, and the admin surface.</p>"""),
            (3, "How paid voting works", """<p><code>castVoteWithPayment</code> is the primary entry point, and it is guarded carefully:</p>
<ul>
<li>It is disabled when the contract is paused.</li>
<li>It requires a non-zero vote cost and that the address has not already paid for this proposal — one paid vote per address.</li>
<li>It transfers the cost from the voter to a configured treasury, or to a burn address when burning is switched on.</li>
<li>It then records the vote, forcing a minimum weight of one so a payment always counts for something.</li>
</ul>
<p>The standard <code>castVote</code> and <code>castVoteWithReason</code> remain available only while free voting is enabled. Once the admin turns free voting off, they revert with a message pointing at the paid path, so there is no quiet way to bypass the gate.</p>"""),
            (4, "Why snapshotting matters more than the gate", """<p>The paid gate makes voting costly for a casual attacker. The snapshot is what makes borrowed-vote attacks structurally impossible.</p>
<p>Vote weight is read from <code>getVotes(voter, block.number - 1)</code> — a past block, not the present. A voter therefore has to hold the tokens before the proposal is raised, not merely at the moment of voting, which removes the entire flash-loan class of attack regardless of how much capital is available.</p>
<p>That is why the contract uses ERC20Votes rather than a plain ERC-20 as its voting source. The gate and the snapshot solve different problems, and only together do they mean anything.</p>"""),
            (5, "Refunds and the treasury", """<p>If a proposal is cancelled, the people who paid to vote on it should not be out of pocket. Cancellation is admin-only and restricted to proposals that are still pending or active — once a proposal has been executed or defeated, the money has already served its purpose.</p>
<p><code>claimRefund</code> requires that the proposal is cancelled, that the caller actually paid, and that they have not already claimed. It returns exactly the cost, and it is idempotent by construction: the <code>hasRefunded</code> flag is set before the transfer.</p>
<p>The destination of the money is a first-class configuration choice. With <code>burnInsteadOfTreasury</code> on, vote payments are destroyed rather than accumulated, which is a deflationary stance a DAO might reasonably prefer. With it off, the treasury accrues and the governor can be funded by its own governance.</p>"""),
            (6, "What I would do differently", """<p>The most valuable part of this project was not the happy path, it was the review. Two things in the committed contract are worth stating plainly, because leaving them unsaid would misrepresent the state of the work:</p>
<ul>
<li>The <code>GovernorSettings</code> constructor receives four positional arguments where the OpenZeppelin version takes three, and the inline comments do not line up with the parameter positions. That is the kind of defect that only a compile and a test run will reliably surface, and it should be corrected and recompiled.</li>
<li>The contract imports <code>Pausable</code> from the <code>security</code> path while the pinned OpenZeppelin version is 5.x, which moved it under <code>utils</code>. Another compile-level break that needs fixing before this can be described as buildable.</li>
</ul>
<p>I am listing these rather than quietly regenerating the repository because the honest version is more instructive. The mechanics are sound and the test suite exists; the build needs a pass, and I would not claim otherwise.</p>
<p>Beyond the fixes, the next real step is deployment and a DAO that actually uses it. A governance contract with no community is a very well-tested hypothesis.</p>"""),
        ],
    },
    {
        "file": "refcrypt-labs.html",
        "title": "Refcrypt Labs Website",
        "meta": "The production client platform for Refcrypt Labs, built with Next.js, Tailwind and a CMS. Source confidential under NDA.",
        "tagline": "A production client platform I build and maintain end to end — documented, since the source is under NDA.",
        "accent": ("ink", "ochre"),
        "title_lines": "          <span>Refcrypt</span>\n          <span>Labs</span>\n          <span>Website</span>",
        "banner_alt": "Abstract artwork in ink and ochre representing the Refcrypt Labs website",
        "credits": [
            ("Role", "Software engineer, web and mobile team"),
            ("Scope", "Front-end architecture · CMS · SEO · Performance · Ongoing maintenance"),
            ("Stack", "Next.js · React · Tailwind CSS · Headless CMS · Vercel"),
            ("Links", '<a class="link" href="https://refcryptlabs.com/" target="_blank" rel="noopener">Live site &#8599;</a> &nbsp;·&nbsp; <span class="muted">Source confidential (NDA)</span>'),
        ],
        "data": [
            ("9", "Service lines presented and maintained on the platform"),
            ("4", "Named products surfaced across the marketing pages"),
            ("2021", "Year the studio was founded; the platform has moved with it since"),
            ("NDA", "Source is client-confidential, so this page documents approach"),
            ("Production", "Live and maintained, with content editable by the team"),
            ("Ongoing", "Maintained rather than delivered and closed"),
        ],
        "body": [
            (1, "The brief", """<p><a href="https://refcryptlabs.com/" target="_blank" rel="noopener">Refcrypt Labs</a> is a software and blockchain studio in Lekki, Lagos, founded in 2021 out of Reffinance. It works across mobile and web development, Web3 integration, smart contracts, data and AI, and the marketing services that surround them — nine service lines in total.</p>
<p>The website has to do something awkward and common: present a broad, technical practice to non-technical buyers, while remaining credible to engineers who will read it. It also has to be maintainable by a small team that is busy with client delivery, which is the constraint that actually drives most of the decisions.</p>
<p>I am on the web and mobile team. I build and maintain this platform alongside client products, and the source is confidential, so what follows is the approach rather than the code.</p>"""),
            (2, "Architecture and the marketing surface", """<p>The platform is a Next.js application with Tailwind for styling, deployed on Vercel. Public pages are rendered so that they arrive fast and are indexable, which matters because a services business with nine offerings lives or dies on search visibility for each of them.</p>
<p>A headless CMS sits behind it. Content — service descriptions, team, products, blog posts — is structured rather than hard-coded, which is what makes the site maintainable by people who are not me. Adding a service line should be a content operation, not a deployment.</p>
<p>The site presents four named products in the studio's orbit and a set of client logos. One deliberate rule I hold to: only publish client names that have been cleared for publication. Unnamed logos are preferable to a claim a client has not agreed to.</p>"""),
            (3, "SEO as a structural concern", """<p>For a services studio, organic search is the primary acquisition channel, so SEO is not a plugin bolted on at the end — it decides the URL structure, the heading hierarchy and the page templates.</p>
<p>In practice that means: one page per service with genuinely distinct content rather than a single features page; semantic headings that reflect the actual content hierarchy; metadata, Open Graph tags and canonical URLs generated per route; and fast pages, because Core Web Vitals are a ranking input as well as a user-experience one.</p>
<p>It also means resisting the temptation to render everything client-side. Content that search engines and social previews need to read should be in the delivered HTML.</p>"""),
            (4, "Maintenance is the real deliverable", """<p>A marketing site is never finished. Service lines change, products launch, the team shifts, copy gets rewritten by people who are better at copy than I am.</p>
<p>So I optimised for the steady state rather than the launch: content that the team can edit, a component structure where a new page is composition rather than invention, and no bespoke mechanism that only one person understands.</p>
<p>The measure of success is not how the site looked on delivery day. It is that months later, the team is still publishing on it without needing to schedule my time.</p>"""),
            (5, "What I would do differently", """<p>The honest note on this project is about tidiness at the edges. A site that is edited continuously accumulates small defects — a dead link in the navigation, placeholder anchors in a footer, a copyright year that stops being updated. They are individually trivial and collectively the difference between a site that feels maintained and one that feels abandoned.</p>
<p>What I would add is a lightweight automated check that runs on every deploy: link validation across the built output, a lint for placeholder or empty hrefs, and a failing build if either appears. Running it in CI means the team cannot reintroduce the problem without noticing, which is more reliable than me remembering to look.</p>
<p>That is the general lesson I keep relearning: quality that depends on someone remembering is not quality, it is luck with a maintenance schedule.</p>"""),
        ],
    },
    {
        "file": "portfolio-builds.html",
        "title": "Client Portfolio Builds",
        "meta": "Three live client portfolio sites delivered for a COO and marketing strategist, built static and mobile-first on Vercel.",
        "tagline": "Three live sites for one client — fast, static, and designed to be edited by the owner.",
        "accent": ("green", "ochre"),
        "title_lines": "          <span>Client</span>\n          <span>Portfolio</span>\n          <span>Builds</span>",
        "banner_alt": "Abstract artwork in green and ochre representing the client portfolio builds",
        "credits": [
            ("Role", "Design and build, sole developer"),
            ("Scope", "Layout · Responsive design · Deployment · Handover"),
            ("Stack", "HTML &amp; CSS · JavaScript · Next.js · Vercel"),
            ("Links", '<a class="link" href="https://rufai-portfolio.vercel.app" target="_blank" rel="noopener">rufai-portfolio &#8599;</a> &nbsp;·&nbsp; <a class="link" href="https://github.com/OlawaleHub/rahmon-portfolio" target="_blank" rel="noopener">rahmon-portfolio &#8599;</a>'),
        ],
        "data": [
            ("3", "Portfolio sites delivered and deployed live"),
            ("5", "Working days from brief to a live domain"),
            ("Static", "Delivery model — no server to maintain or pay for"),
            ("Mobile-first", "Designed at the small breakpoint and scaled up"),
            ("100%", "Pages that test as responsive across common breakpoints"),
            ("0", "Recurring hosting cost on the client's side"),
        ],
        "body": [
            (1, "The brief", """<p>A COO and marketing strategist needed a professional web presence — somewhere to send recruiters and conference contacts that was not a PDF attachment or a LinkedIn profile.</p>
<p>The requirements were refreshingly practical: it should load quickly, look credible on a phone, be easy to point a domain at, and not require a monthly bill or a maintenance relationship afterwards. This is the kind of brief where the right answer is usually the smallest thing that works.</p>
<p>I delivered three iterations across the same engagement as the content and positioning were refined.</p>"""),
            (2, "Why static was the right call", """<p>For a portfolio site with a handful of pages and content that changes a few times a year, a database and a server are pure overhead. Every one of them is something that can go down, cost money, or need a security patch.</p>
<p>Static files on a CDN sidestep all of it. The pages are pre-built, the hosting is effectively free at this scale, the attack surface is close to nil, and there is no server to keep awake. It is the rare case where the technically simplest option is also the fastest and the cheapest.</p>
<p>One of the builds went further and used Next.js where the layout benefited from a component structure; the others are straightforward HTML and CSS. Choosing per project rather than by habit is the point.</p>"""),
            (3, "Designed at 375 pixels first", """<p>The primary device for this audience is a phone — someone opening a link from an email or a WhatsApp message while commuting. Designing at desktop width and then squeezing it down produces exactly the wrong result: text that is too small, navigation that collapses badly, and images that dominate the first screen.</p>
<p>So every layout starts at the narrow breakpoint. Type sizes, tap targets and spacing are chosen there, then allowed to breathe as the viewport grows. The desktop version is the enhancement, not the origin.</p>
<p>That approach also enforces discipline about content. If a section cannot justify its space on a 375-pixel screen, it usually cannot justify it on a 1440-pixel one either.</p>"""),
            (4, "Handover and ownership", """<p>The most important design decision on a project like this is what happens after I stop working on it. A portfolio that only its developer can update is a liability, not an asset — the client ends up emailing me to change a job title.</p>
<p>So the content lives in plain, readable markup with clear section boundaries, and I walked the client through editing it directly. Where a change was likely to be recurring, I optimised for that specifically rather than for elegance in the abstract.</p>
<p>Each site was deployed to a live domain with HTTPS and a build that reruns automatically on push, so publishing is a matter of editing a file.</p>"""),
            (5, "What I would do differently", """<p>Three iterations of the same site is two more than necessary, and the reason was process rather than craft: I started building before the content and positioning were settled, so each round of copy changes became a round of layout changes.</p>
<p>The fix is not more design tooling. It is refusing to start until the actual text exists, because real sentences break layouts in ways placeholder text never does. Placeholder content flatters every design.</p>
<p>I would also add analytics and a contact-form fallback from day one. Without a way to see whether visitors reach the contact page, both the client and I are guessing about which sections are earning their place — and guessing is what you do when you did not instrument the thing.</p>"""),
        ],
    },
    {
        "file": "mobile-flutter.html",
        "title": "Cross-platform Mobile with Flutter",
        "meta": "Cross-platform mobile development in Dart and Flutter — clean architecture, state management, API integration and release builds.",
        "tagline": "One codebase, two platforms, and architecture chosen so it still reads well in a year.",
        "accent": ("carmine", "ink"),
        "title_lines": "          <span>Cross-platform</span>\n          <span>Mobile</span>\n          <span>with Flutter</span>",
        "banner_alt": "Abstract artwork in carmine and ink representing cross-platform Flutter development",
        "credits": [
            ("Role", "Mobile engineering, web and mobile team"),
            ("Scope", "Architecture · State management · API integration · Local persistence · Release builds"),
            ("Stack", "Dart · Flutter · REST APIs · Firebase · Android Studio · iOS &amp; Android targets"),
            ("Links", '<span class="muted">Client work — source confidential</span>'),
        ],
        "data": [
            ("2", "Platforms from a single Dart codebase"),
            ("1", "Codebase to maintain rather than two native projects"),
            ("Clean", "Architecture, so features are added rather than patched in"),
            ("Released", "Built and shipped to real users, not prototypes"),
            ("Ongoing", "Maintained as part of my role at Refcrypt Labs"),
            ("Dart", "Primary language across all mobile work"),
        ],
        "body": [
            (1, "Why Flutter for this work", """<p>The alternative to Flutter is either two native codebases or a web view, and neither is right for a small team shipping a real product. Two codebases means every feature is built twice and every bug is fixed twice. A web view means giving up on the things that make a mobile app worth installing in the first place.</p>
<p>Flutter gives one Dart codebase that compiles to native on both platforms, with a consistent rendering model rather than a thin wrapper over platform widgets. For a team of our size, halving the surface area is worth more than any single-platform advantage.</p>
<p>The trade-off is honest and worth stating: platform-specific behaviour still needs platform-specific code, and anyone who tells you otherwise has not shipped an app with background location or push notifications.</p>"""),
            (2, "Architecture before features", """<p>The temptation on a mobile project is to start with the screens, because screens are what you can show somebody. The cost of that choice arrives about six months in, when every new feature requires understanding the whole app.</p>
<p>So I structure by feature rather than by layer: each feature owns its own presentation, logic and data access, and depends on shared abstractions rather than on other features. Adding a feature means adding a directory, not editing five.</p>
<p>The payoff is concrete. Onboarding a second developer is faster, tests stay local to the thing they test, and deleting a feature is a deletion rather than an archaeology exercise.</p>"""),
            (3, "State management as a decision, not a default", """<p>State management is where Flutter projects most often go wrong, usually because a solution was adopted before the problem was understood. The question to answer first is not &ldquo;which library&rdquo; but &ldquo;what kind of state is this&rdquo;.</p>
<p>Server data that can be cached and needs to survive navigation is a different problem from ephemeral UI state, and different again from app-wide session state. Treating all three the same way produces either an anaemic app or an unmaintainable one.</p>
<p>I keep the rules explicit and consistent, so that a new screen's state has an obvious home and there is no argument about it in review. Consistency matters more here than picking the theoretically optimal tool.</p>"""),
            (4, "The unglamorous mobile work", """<p>Most of the difficulty in a shipped mobile app is not in the feature list. It is in the parts that only appear on real devices on real networks:</p>
<ul>
<li><strong>Poor connectivity</strong> — requests that fail halfway, timeouts that need to be distinguished from genuine errors, and retries that must not duplicate a write.</li>
<li><strong>Lifecycle</strong> — the app being backgrounded mid-request, or killed and restored, and what the user should see when that happens.</li>
<li><strong>Permissions</strong> — camera, location and notifications, each of which can be refused, and none of which should be a dead end.</li>
<li><strong>Release mechanics</strong> — signing, build flavours, versioning and the store submission path, which is where a surprising amount of project time quietly goes.</li>
</ul>
<p>None of this is exciting and all of it determines whether the app feels reliable. Users do not distinguish between a feature that was never built and one that crashes when they open it.</p>"""),
            (5, "What I would do differently", """<p>Two things I would change on the next mobile project.</p>
<p>First, I would set up automated device testing much earlier. Manual testing across a handful of physical devices does not scale, and the bugs that escape are predictably the ones involving interruption and resumption — the exact scenarios that manual testing does not naturally reproduce.</p>
<p>Second, I would instrument performance from the first internal build rather than after launch. Frame times, cold-start duration and memory behaviour are far easier to keep good than to make good retrospectively, and by the time a user complains about jank you have usually accumulated a dozen causes rather than one.</p>
<p>The broader lesson from this work is that cross-platform development rewards discipline more than cleverness. One codebase is a genuine advantage, and only if you resist the temptation to let it become two overlapping ones held together by conditionals.</p>"""),
        ],
    },
]

# ---------------------------------------------------------------- render

def render(index: int, project: dict) -> str:
    last = index == len(PROJECTS) - 1
    nxt = PROJECTS[(index + 1) % len(PROJECTS)]
    a, b = project["accent"]
    credits = "\n".join(
        f'          <div class="credit-row">\n'
        f'            <dt class="label">{k}</dt>\n'
        f'            <dd class="credit-value">{v}</dd>\n'
        f'          </div>'
        for k, v in project["credits"]
    )
    data_rows = "\n".join(
        f'          <div class="data-row">\n'
        f'            <div class="data-figure">{fig}</div>\n'
        f'            <div class="data-label">{lab}</div>\n'
        f'          </div>'
        for fig, lab in project["data"]
    )
    sections = []
    for num, heading, body in project["body"]:
        sections.append(
            f'      <section class="cs">\n'
            f'        <div class="cs-head">\n'
            f'          <span class="cs-num label">{num:02d}</span>\n'
            f'          <h2 class="cs-title">{heading}</h2>\n'
            f'        </div>\n'
            f'        <div class="cs-body prose">\n{body}\n        </div>\n'
            f'      </section>'
        )
    return SHELL.format(
        title=project["title"],
        meta=project["meta"],
        index=index + 1,
        next_file="../portfolio.html" if last else nxt["file"],
        next_title="Back to the full index" if last else nxt["title"],
        folio_next="Index" if last else "Next",
        banner=banner_svg(ACCENT[a], ACCENT[b]),
        banner_alt=project["banner_alt"],
        title_lines=project["title_lines"],
        tagline=project["tagline"],
        credits=credits,
        data_rows=data_rows,
        body="\n\n".join(sections),
    )


written = []
for i, project in enumerate(PROJECTS):
    path = OUT / project["file"]
    path.write_text(render(i, project), encoding="utf-8")
    written.append((project["file"], len(path.read_text(encoding="utf-8"))))

for name, size in written:
    print(f"{name:28} {size:>7} bytes")
print(f"\n{len(written)} case-study pages written to {OUT}")
