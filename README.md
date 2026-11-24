# Made99

**Made (1999 version).** Made is a personal graphics and demoscene site from 1999, with an entry page, a framed portal page and sections for news, digital art (party flyers and t-shirt designs), a gallery of pictures in period formats (GIF, PCX, TGA, TIF) with downloadable packs, an about-me page and a links page.

Archive of an old static website, served as-is from bunny.net at the hostname
of [`site.json`](site.json). Kept online for history, no longer developed.

Full list of the sites: https://chanoj.github.io/

## Changes from the original site

The files are as served in 1999, apart from the changes needed to run in a modern browser:

- `index.html` is now only the entry page (credits and an enter link). The framed site page
  (`portal.html` in an iframe) moved to `site.html`: it used to open as a popup, which browsers
  block. It shows an OS-like window frame on desktop (Windows 10/11, macOS 2012 to 2026, picked
  from the user agent) and scales to the screen on mobile, with a rotate hint in portrait.
  `?os=win10|win11|mac2012|mac2014|mac2020|mac2026` and `?device=mobile|desktop` force a look.
- The obsolete browser sniffing script and alerts were dropped.
- The banner image `ban460x55.gif`, absent from the archive, is no longer referenced.
- The section pages (`d_art`, `ffuture`, `files`, `links`, `me`, `news`) declare their
  windows-1252 charset (`<meta charset>`), which the host does not send, so accents display
  correctly. The page bytes are otherwise unchanged.

## Search engines

`scripts/seo.py` writes `robots.txt` (allow everything, with the `Sitemap:` line) and `sitemap.xml` (indexable pages only) into `site/`; run `python3 -I scripts/seo.py` after any change of `site/`.

The site pages are shown in the window of `site.html`. `scripts/frame-restore.js` (one `<script>` tag in every page, added by `seo.py`) sends a page opened on its own (a search result) to `site.html#p=<page>`, which loads it in the iframe; the page stays a plain file, so crawlers still read it.

## Layout

| Path | Content |
| --- | --- |
| `site/` | The website files, exactly as served (imported from the storage zone) |
| `site.json` | The only site-specific settings: repository, storage zone, pull zone, hostname (plus zone ids, only until the first apply adopts them) |
| `infra/` | OpenTofu: storage zone, pull zone, hostname (state encrypted, committed) |
| `infra/secrets.env` | Proton Pass **references** to the secrets (vault `OldSites`), no secret values |
| `scripts/deploy.py` | Sync `site/` to the storage zone, purge the CDN |
| `scripts/smoke_test.py` | Check that the public site serves the files of `site/` |
| `scripts/bootstrap.sh` | Set up a new repository of the same kind (see below) |
| `scripts/import_storage.py` | One-time download of the storage zone into `site/` |

DNS is not managed here: the hostname is a CNAME to `<pull zone>.b-cdn.net`
at Infomaniak.

## Removal requests

Pages that list or describe people end with a small footer, "To be removed from this page, contact me." (a `mailto:` link). `scripts/add_removal_note.py` adds it to the pages it lists (idempotent; `--check` reports pages that lack it).

## Deploying

- **Website**: push a change under `site/` to `main` → workflow *Website: deploy*
  uploads the changed files, deletes the removed ones, purges the CDN and runs
  the smoke test. A manual run allows a dry run.
- **Infra**: pull requests touching `infra/` show the plan; apply is a manual
  run of *Infra: bunny.net* (action `apply`, from `main`), which commits the
  encrypted state.

GitHub secrets: `BUNNY_API_KEY` (bunny.net account API key) and
`TF_VAR_STATE_PASSPHRASE` (state encryption), both from Proton Pass vault
`OldSites`. The storage zone password and pull zone id are looked up from the
API key, never stored.

Locally (Proton Pass CLI logged in):

```bash
pass-cli run --env-file infra/secrets.env -- python3 scripts/deploy.py --dry-run
```

```bash
cd infra && pass-cli run --env-file secrets.env -- tofu plan
```

## Reuse for another site

The same files serve every old site of the bunny.net account; only `site.json`,
`site/`, the README title and the passphrase reference differ.

1. Copy the template into the new, empty repository folder (here `HotDIR97`):

   ```bash
   cd ~/Code/OrangeJuice97 && git ls-files | grep -v -e '^site/' -e '^site.json$' -e '^infra/terraform.tfstate$' | rsync -a --files-from=- . ~/Code/HotDIR97/
   ```

2. Fill in the site-specific parts, download the files and check everything
   (plan, deployment dry run, smoke test):

   ```bash
   cd ~/Code/HotDIR97 && git init -b main && scripts/bootstrap.sh init HotDIR97 chandra-sw chandra
   ```

3. Create the GitHub repository and its secrets, then push and run the
   *Infra: bunny.net* workflow with action `apply` (adopts the existing
   resources into the state):

   ```bash
   scripts/bootstrap.sh github
   ```

4. Once the first apply has adopted the resources, rename the zones after the
   repository (bunny.net cannot rename: the zones are replaced, new ones first):
   - at Infomaniak, point the CNAME of the hostname to `<repo, lowercase>.b-cdn.net`
     (any `*.b-cdn.net` name reaches bunny.net, which routes by hostname, so
     this is safe before and after the switch);
   - one pull request that removes the ids from `site.json` and sets
     `storage_zone` and `pullzone` to the lowercase repository name;
   - after merge, run *Infra: bunny.net* with action `apply`: it creates the
     new zones, moves the hostname, deletes the old zones, deploys `site/` to
     the new storage zone and runs the smoke test (a few minutes of errors at
     most, while the files are uploaded and the certificate issued).

## To Do

Cross-links to fix in a batch pass (the targets are archived on `sauthier.family`; rewrite the `href`s):

- `ojuice.planet-d.net` (1 link): Orange Juice 1999 (https://orangejuice99.sauthier.family).
