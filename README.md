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
| Experience | [LinkedIn](https://www.linkedin.com/in/sakshi-bhati/) — **could not be fetched automatically** (login wall) |

## Placeholders to fill in

Search `index.html` for `PLACEHOLDER`:

- **Photo** — save a portrait as `assets/sakshi-bhati.jpg` and replace the `.photo-placeholder` div with
  `<img src="assets/sakshi-bhati.jpg" alt="Portrait of Dr. Sakshi Bhati">`.
- **Experience** — the highlighted (yellow) entry in the Experience list; add roles from LinkedIn.

- **Brand copy to review**: the hero headline ("Communication that includes everyone."), section headlines, and the press-kit short bio were written for this site from her SIU bio. Confirm or adjust them.

Citation counts and the "9 publications" stat are snapshots; update the numbers in the Publications section periodically.

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
