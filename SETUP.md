# Terminal Profile & Cyber Vector Dashboard — Setup & Maintenance

This repository houses the terminal-dashboard GitHub profile system for **Abhay Pratap Singh** (`dexterbeast0-cmyk/dexterbeast0-cmyk`). It autonomously generates a high-resolution character-density vector portrait (`ascii.svg`), an animated ASCII wordmark (`name.svg`), and a complete suite of glossy glassmorphic dashboard cards (`assets/cards/`) driven by live GitHub telemetry.

---

## 1. Directory Structure

```text
dexterbeast0-cmyk/
│
├── .github/
│   └── workflows/
│       └── portrait.yml         # CI/CD workflow (daily schedule + push triggers)
│
├── assets/
│   ├── profile-pro.jpg          # Primary studio portrait source photo
│   ├── profile.jpg              # Secondary reference portrait
│   └── cards/                   # Glassmorphic cyber terminal dashboard cards
│       ├── card-profile.svg     # Identity card with identicon & reticle
│       ├── card-highlights.svg  # Top highlights card
│       ├── card-signal.svg      # Live metrics & stats telemetry
│       ├── card-stack.svg       # Language distribution stack
│       ├── card-work.svg        # Pinned projects & progress gauges
│       ├── card-activity.svg    # 52-week activity heatmap
│       └── card-contact.svg     # Connect button with GitHub handle
│
├── data/
│   └── github.json              # Normalized live GitHub profile telemetry
│
├── scripts/
│   ├── make_portrait.py         # Master entrypoint for profile asset regeneration
│   ├── generate_cards.py        # Glassmorphic card & terminal window rendering engine
│   ├── build_ascii_name.py      # High-density ASCII nameplate generator
│   └── fetch_github_data.py     # Live GitHub telemetry collector
│
├── ascii.svg                    # Hero terminal scan (VISUAL.MAP + SYSTEM.INFO)
├── name.svg                     # Animated ASCII wordmark (ABHAY PRATAP SINGH)
├── README.md                    # Terminal/cyber developer dashboard
├── requirements.txt             # Dependencies (Pillow>=10.0.0)
├── SETUP.md                     # Documentation & maintenance guide
└── .gitignore                   # Ignored files (test.mp4, cache, scratch)
```

---

## 2. Local Setup & Quickstart

### Prerequisites
- **Python 3.10+**
- **pip**

### Installation
Clone or navigate into the workspace:

```bash
cd dexterbeast0-cmyk
```

Install requirements:
```bash
pip install -r requirements.txt
```

---

## 3. How to Run the Generators

### Fetch Live GitHub Telemetry:
```bash
python scripts/fetch_github_data.py
```
Fetches real data from the GitHub API and writes normalized metrics to `data/github.json`.

### Regenerate All Profile Assets:
```bash
python scripts/make_portrait.py
```
This command:
1. Loads `data/github.json`.
2. Generates `name.svg` via `scripts/build_ascii_name.py`.
3. Segments `assets/profile-pro.jpg` and produces `ascii.svg` with live telemetry.
4. Renders the complete suite of glassmorphic cards in `assets/cards/`.

---

## 4. How the Telemetry Pipeline Works

1. **Data Collection (`scripts/fetch_github_data.py`)**:
   - Queries GitHub REST API for user profile metrics (`public_repos`, `followers`, `following`, `created_at`).
   - Analyzes public repositories to calculate real star counts, language bytes, and project metadata.
   - Fetches public contribution calendar data (total contributions, active days, and 52x7 week cells).
   - Writes normalized, deterministic JSON to `data/github.json`.
   - **Failure Safety**: If the GitHub API fails or rate-limits, existing telemetry in `data/github.json` is preserved without overwriting valid data with zeroes.

2. **Card Generation (`scripts/generate_cards.py`)**:
   - Reads `data/github.json` and renders live numbers into all cards:
     - `ascii.svg`: Shows real repository counts, stars, contributions, and active days alongside the ASCII face.
     - `card-profile.svg`: Shows authentic username and handle.
     - `card-highlights.svg`: Shows real public repository count and featured repository.
     - `card-signal.svg`: Displays live metrics for Stars, Contributions, Repos, and Followers.
     - `card-stack.svg`: Visualizes repository-weighted programming languages.
     - `card-work.svg`: Displays real public projects and metadata.
     - `card-activity.svg`: Renders authentic contribution heatmap cells and total count.

---

## 5. How the Portrait is Generated

1. **Source Photo**: The generator reads `assets/profile-pro.jpg`.
2. **Background Segmentation**: Multi-point edge flood-filling and color-distance analysis isolate the subject from the backdrop, fading smoothly into the terminal canvas `#040d12`.
3. **Contrast & Edge Enhancement**: Fine unsharp masking and inverted edge blending emphasize facial contours, eyes, and jawline definition.
4. **Calibrated Monospace Ramp**: Pixels are mapped to high-density monospace glyphs (` .:-=+*cso#%8&S@`) across 160 columns at an aspect ratio factor of 0.51.
5. **Dual-Panel Integration**: Embedded into `VISUAL.MAP` (left) alongside `SYSTEM.INFO` (right) with live telemetry.

### How to Replace the Portrait
To update your portrait photo:
1. Replace `assets/profile-pro.jpg` with your new studio headshot.
2. Run `python scripts/make_portrait.py`.
3. Commit and push the changes.

---

## 6. How the Name is Generated

The name banner (`name.svg`) is engineered using high-density character-matrix typography matching the aesthetic of the facial ASCII art:
1. **Normalized Matrix**: Each character in `ABHAY PRATAP SINGH` is constructed on a 12-column normalized monospace grid using density-mapped ASCII characters (`8`, `:`, `.`, `'`).
2. **Soft Grey Base Palette**: Styled in `#C9D1D9` (primary) and `#F0F6FC` (highlight), matching GitHub's dark theme and terminal text.
3. **Infinite SMIL Loop**:
   - **0.0s – 3.0s**: Progressive left-to-right letter reveal (`A` → `AB` → ... → `ABHAY PRATAP SINGH`) synchronized with a vertical scanning laser beam.
   - **3.0s – 3.5s**: Complete name hold.
   - **3.5s – 4.3s**: Glossy specular cyan reflection sweep across the full name.
   - **4.3s – 5.0s**: Graceful fade reset returning to the start state.
4. **Zero-Clipping Responsive ViewBox**: Rendered inside `viewBox="0 0 960 96"` with 22px margin inside corner brackets (`x=50.0` to `x=910.9`), ensuring full visibility across all device widths.

---

## 7. GitHub Actions CI/CD Automation

The automated workflow in `.github/workflows/portrait.yml` runs:
1. **Daily on Schedule**: Every day at 02:17 UTC (`17 2 * * *`) to fetch fresh GitHub statistics.
2. **On Push**: When changes occur to `assets/profile-pro.jpg`, `scripts/**`, or `requirements.txt`.
3. **Manual Trigger**: Supports `workflow_dispatch` for on-demand refreshes directly from the GitHub Actions tab.

### Change Detection & Loop Prevention:
- Executes `git diff --staged --quiet`. If telemetry and SVGs have not changed, the workflow exits cleanly with zero commits.
- If changes are detected, commits with `[skip ci]` to prevent infinite recursive runs.
