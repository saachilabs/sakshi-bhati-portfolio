# Dr. Sakshi Bhati — Portfolio

Static single-page portfolio for Dr. Sakshi Bhati, Assistant Professor of Public Relations & Leadership, Communication Studies, Southern Illinois University Carbondale.

Plain HTML/CSS/JS, no build step. Designed as a personal-brand / media-kit site for a PR professor: positioning headline, proof-point stats bar, research message pillars, press-style award feature, a copy-ready press bio, and a speaking & media call to action. Uses SIU maroon (`#720000`) with white and warm neutrals.

```
index.html      page content (all sections)
css/styles.css  styles (colors defined as CSS variables at the top)
js/main.js      mobile nav, publication sorting, copy-bio button, active-section highlighting
assets/         images (add the portrait here)
.nojekyll       tells GitHub Pages to serve files as-is
```

## Content sources

| Section | Source |
| --- | --- |
| Bio, title, contact, education | [SIU faculty profile](https://faculty.siu.edu/profiles/a-c/bhati-sakshi.php) |
| Publications, citation metrics | [Google Scholar](https://scholar.google.com/citations?user=x6gjq2cAAAAJ&hl=en) |
| Top Paper Award | [K-State news](https://www.k-state.edu/media-communication/about/news/Bhati-Top-Paper-Award.html) |
| Certification, skills, SIU awards | Provided from her [LinkedIn](https://www.linkedin.com/in/sakshi-bhati/) |
| Experience | LinkedIn — **could not be fetched automatically** (login wall) |
| Harvard shield (`assets/harvard-shield.svg`) | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Harvard_shield-University.svg), public domain file; Harvard marks are trademarks, used here only to identify the certification issuer |

## Placeholders to fill in

Search `index.html` for `PLACEHOLDER`:

- **Photo** is at `assets/sakshi-bhati.jpg` (square). Replace the file to update it; a higher-resolution square image (600px+) will look sharper.
- **Experience** — the highlighted (yellow) entry in the Experience list; add roles from LinkedIn.

- **Brand copy to review**: the hero headline ("Communication that includes everyone."), section headlines, and the press-kit short bio were written for this site from her SIU bio. Confirm or adjust them.



## Google Scholar sync

Citation counts, h-index, i10-index, the publication count, the "most cited" feature and the publication list are refreshed automatically from her [Google Scholar profile](https://scholar.google.com/citations?user=x6gjq2cAAAAJ&hl=en).

- `.github/workflows/update-scholar.yml` runs `scripts/update_scholar.py` every Monday and Thursday (and on demand: **Actions → Update Google Scholar data → Run workflow**). It commits only when something changed, and GitHub Pages redeploys.
- The script rewrites only the marked parts of `index.html` (`data-scholar="..."` elements and `<!-- scholar:...:start/end -->` blocks), using the same markup as the rest of the page. Don't hand-edit inside those markers; edits there are overwritten.
- `data/scholar.json` holds the last successful fetch.
- **Formatting:** new papers are formatted automatically (initials like `A. M. Mason`, her name in bold, journal in title case and italics, `26(10), 667–674`). To fix a title, venue or label, add an entry to `data/publication-overrides.json` keyed by the Scholar citation id (shown in the workflow log as `New publication: ... (id ...)`). Set `"hide": true` to drop an entry.
- **When Scholar blocks the request:** Scholar has no API and sometimes serves a CAPTCHA to GitHub's servers. The run then logs a warning and changes nothing, so the site keeps the last good numbers; the "updated" date under the publication list shows when data was last refreshed. Scraping Scholar is against its terms of service; it is used here at low volume (two requests a week).

Run it locally with `python3 scripts/update_scholar.py` (Python 3 standard library only).

## Local development

No dependencies required. Serve the folder with any static server:

```bash
python3 -m http.server 8000
# or: npx serve .
```

Then open http://localhost:8000. (Opening `index.html` directly also works.)

## Deploy to GitHub Pages

1. Push this repo to GitHub (branch `main`).
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to *Deploy from a branch*, branch `main`, folder `/ (root)`, and click **Save**.
4. After a minute the site is live at `https://<owner>.github.io/sakshi-bhati-portfolio/`.

Optional custom domain: add it under **Settings → Pages → Custom domain** (this creates a `CNAME` file) and point a DNS `CNAME` record to `<owner>.github.io`.
