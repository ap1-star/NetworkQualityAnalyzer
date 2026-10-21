# ECE Recruitment Radar — GATE 2027

Standalone dashboard for PSU GATE and non-GATE jobs, space/defence/research roles, UPSC ESE, SSC, Railway recruitment and state AE/JE notices. Built inside `ece-recruitment-radar/` to avoid replacing files in the existing NetworkQualityAnalyzer project.

## Publishing and live updates
- The GitHub Pages workflow publishes this folder as the site root at `https://ap1-star.github.io/NetworkQualityAnalyzer/`.
- The crawler checks 59 official recruitment/exam pages every six hours using GitHub Actions and updates `data/live-notices.json`.
- Once merged to the default branch, both workflows run on relevant pushes. If Pages deployment is blocked because Pages has not yet been enabled, open repository Settings → Pages and select GitHub Actions as the source, then rerun the deploy workflow in Actions.
- You may start a crawl manually via Actions → Refresh official recruitment feed → Run workflow.
- The dashboard also fetches the feed each time it is opened and when Check feed is pressed.

## Accuracy limits
This is link discovery, not a guarantee of every vacancy. It doesn't auto-certify ECE eligibility, route (GATE/non-GATE), open/closed application status, salary, age rules or deadlines. New links are labelled unverified until a user opens the original notification/PDF. Pages can block crawlers, render data with JavaScript, or publish notices on additional sub-sites; review source health and add missing official pages to `data/sources.json`.

Shortlist, task checks and per-notice progress are saved to the browser's local storage on the device where you use the site. They are not synced between devices in this version.
