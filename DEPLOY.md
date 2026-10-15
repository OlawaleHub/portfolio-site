# Deploying to Vercel

The site is fully static — no build step, no dependencies, 40 tracked files,
about 0.5 MB. Vercel will serve it as-is.

Everything below assumes you are deploying the **`portfolio-soliu`** folder.

---

## Current state of this folder

Already done, so you do not need to repeat it:

- A local git repository exists, on branch `main`
- One clean commit: *"Portfolio site: editorial grid design system, 11 pages, 6 case studies"*
- 40 files tracked, working tree clean, `.gitattributes` normalising line endings
- Your git identity is set **for this repository only**, not globally

Still to do: create the GitHub repo, push to it, connect Vercel.

> If you want your identity available in *every* project, run these once. The
> global config could not be written from the build environment:
>
> ```powershell
> git config --global user.name "Soliu Quadri"
> git config --global user.email "quadrisoliu14@gmail.com"
> ```

---

## I just want the link — Option A, drag and drop (~1 minute)

This skips GitHub entirely. You need a Vercel account (free, sign up with
GitHub, GitLab, Bitbucket or email).

1. Go to **<https://vercel.com/new>**
2. Look for the **"Deploy" / "Upload"** area. If you see a Git-provider list
   instead, look for the link underneath it that says something like
   *"Want to deploy a template? / Or upload a folder"* — Vercel tucks the
   uploader here and the label changes occasionally.
3. **Drag the `portfolio-soliu` folder** onto the upload area.
   - Drag the **folder itself**, not a zip and not the individual files inside it.
   - Vercel requires `index.html` at the root of what you upload. If you
     accidentally drag the *contents*, you get a 404.
4. Vercel detects the framework as **Other** and shows no build command. That is
   correct — leave everything alone.
5. Click **Deploy**.
6. You get a URL like `portfolio-soliu-abc123.vercel.app` within a few seconds.

**Caveat on drag-and-drop:** this creates a *deployment* but not a *project you
can update*. To change the site later you either drag it again (new URL) or move
to Option B.

---

## Option B — GitHub import (recommended, gives you auto-redeploys)

This gives you a permanent project: every `git push` publishes automatically.

### Fastest way: run the helper script

```powershell
cd portfolio-soliu
powershell -ExecutionPolicy Bypass -File .\deploy-to-github.ps1
```

It checks git, verifies your identity, commits anything outstanding, prompts for
your GitHub username, pushes, and prints the Vercel steps at the end. Safe to
re-run — later runs just push whatever changed.

If Windows blocks it with *"running scripts is disabled on this system"*, the
`-ExecutionPolicy Bypass` flag above is the fix.

### Or do it by hand

The repository and first commit already exist, so you only need the remote:

```powershell
cd portfolio-soliu

# 1. Create an EMPTY repo at https://github.com/new
#    Name it "portfolio". Do NOT add a README, .gitignore or licence.

# 2. Point this repo at it (use your own username)
git remote add origin https://github.com/OlawaleHub/portfolio.git

# 3. Push
git push -u origin main
```

When Git asks for a password, **your GitHub account password will not work**.
Create a Personal Access Token instead: <https://github.com/settings/tokens> →
*Generate new token (classic)* → tick the `repo` scope → paste the token as the
password. Git's Windows credential manager will remember it.

The smoother alternative is GitHub CLI, which handles the login for you:

```powershell
winget install --id GitHub.cli
gh auth login
```

### Then import it into Vercel

1. Go to **<https://vercel.com/new>**
2. Under **Import Git Repository**, find the repo you just pushed and click
   **Import**. (If it is not listed, click *Adjust GitHub App Permissions* and
   grant access to that repo.)
3. On the configuration screen:
   - **Framework Preset:** Other
   - **Root Directory:** `./` — leave as is
   - **Build Command:** leave empty / override is off
   - **Output Directory:** leave empty
   - **Install Command:** leave empty
4. Click **Deploy**.

You will get a stable URL such as `portfolio.vercel.app`.

### 3. Updating the site

```powershell
# edit files, then:
git add .
git commit -m "Update the Lagos Emergency case study"
git push
```

Vercel rebuilds and republishes in about ten seconds.

### 4. Adding a custom domain

In the project: **Settings → Domains → Add**. Point an `A` record to
`76.76.21.21` or a `CNAME` to `cname.vercel-dns.com` at your registrar. Vercel
issues the TLS certificate automatically.

---

## What `vercel.json` does

It is committed and Vercel reads it automatically:

- `"framework": null` — stops Vercel guessing at a Next.js project. This is a
  plain static site, so there is nothing to build.
- `"cleanUrls": true` — serves `/about` instead of `/about.html` and redirects
  the `.html` form. All internal links are relative, so they keep working.
- `"trailingSlash": false` — keeps `/work/lagos-emergency` clean. Relative
  asset paths (`../assets/...`) resolve correctly either way.
- A long-lived `Cache-Control` header on `/assets/**`, since those files are
  content-stable and fingerprinted by name.

`.vercelignore` keeps the `_build/` helper scripts, this documentation, and
local tooling out of the published output. It is not strictly required — Vercel
only *serves* the HTML and assets — but it keeps the deployment tidy.

---

## If something goes wrong

**"404: NOT_FOUND" on the root URL**
You uploaded the wrong level. Vercel needs `index.html` at the root of the
upload, so drag the `portfolio-soliu` folder itself.

**Pages load but have no styling**
The CSS did not upload. Check that `assets/css/site.css` exists in the deployed
file list under **Deployments → your deployment → Source**.

**Blank or unstyled page in Safari/Firefox but fine in Chrome**
Unlikely here — there is no build step and no transpilation. If it happens,
check for a browser extension blocking the Google Fonts request.

**Fonts look wrong**
Fonts load from `fonts.googleapis.com`. They will render as system fallbacks if
that request is blocked, which is a graceful degradation, not a failure.

**A case study 404s**
Case studies live in `work/` and are linked as `work/lagos-emergency.html`
(relative). With `cleanUrls`, Vercel also answers `/work/lagos-emergency`. If
you renamed a file, update the link in `portfolio.html` and `index.html`, then
re-run `_build/build_cases.py` if it was a generated page.

---

## Re-deploying after content edits

Nothing special is required for hand-edited pages — commit and push.

If you edited the **generated** case studies, rebuild them first:

```powershell
& "C:\Users\USER\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" `
  _build\build_cases.py
```

Then commit. And before pushing, it is worth running the two checkers:

```powershell
& $py _build\verify_site.py          # needs a server on 127.0.0.1:8899
& $py _build\validate_structure.py
```
