# Terminal Profile & Cyber Vector Dashboard — Setup & Maintenance

This repository houses the terminal-dashboard GitHub profile system for **Abhay Pratap Singh** (`dexterbeast0-cmyk/dexterbeast0-cmyk`). It autonomously generates a high-resolution character-density vector portrait (`ascii.svg`), an animated ASCII wordmark (`name.svg`), and a complete suite of glossy glassmorphic dashboard cards (`assets/cards/`).

---

## 1. Directory Structure

```text
dexterbeast0-cmyk/
│
├── .github/
│   └── workflows/
│       └── portrait.yml         # CI/CD workflow to regenerate profile assets
│
├── assets/
│   ├── profile-pro.jpg          # Primary source portrait photo
│   ├── profile.jpg              # Original / backup portrait reference
│   └── cards/                   # Glassmorphic cyber terminal dashboard cards
│       ├── card-profile.svg     # Identity card with identicon & reticle
│       ├── card-highlights.svg  # Top highlights card
│       ├── card-signal.svg      # Live metrics & stats telemetry
│       ├── card-stack.svg       # Language distribution stack
│       ├── card-work.svg        # Pinned projects & progress gauges
│       ├── card-activity.svg    # 52-week activity heatmap
│       └── card-contact.svg     # Connect button with GitHub handle
│
├── scripts/
│   ├── make_portrait.py         # Master entrypoint for profile asset regeneration
│   ├── generate_cards.py        # Glassmorphic card & terminal window rendering engine
│   └── build_ascii_name.py      # High-density ASCII nameplate generator
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

## 3. How to Run the Generator

To regenerate all profile assets (`name.svg`, `ascii.svg`, and all cards in `assets/cards/`):

```bash
python scripts/make_portrait.py
```

This single command:
1. Generates `name.svg` via `scripts/build_ascii_name.py`.
2. Segments `assets/profile-pro.jpg` and produces `ascii.svg` with live telemetry.
3. Renders the complete suite of glassmorphic cards in `assets/cards/`.

---

## 4. How the Portrait is Generated

1. **Source Photo**: The generator reads `assets/profile-pro.jpg`.
2. **Background Segmentation**: Multi-point edge flood-filling and color-distance analysis isolate the subject from the backdrop, fading the boundary smoothly into the terminal canvas `#040d12`.
3. **Contrast & Edge Enhancement**: Fine unsharp masking and inverted edge blending emphasize facial contours, eyes, and jawline definition.
4. **Calibrated Monospace Ramp**: Pixels are mapped to high-density monospace glyphs (` .:-=+*cso#%8&S@`) across 160 columns at an aspect ratio factor of 0.51.
5. **Dual-Panel Integration**: The segmented portrait is embedded into the left panel (`VISUAL.MAP`) while the right panel (`SYSTEM.INFO`) renders a cyber telemetry console with dotted-leader metrics.

### How to Replace the Portrait
To update your portrait photo:
1. Replace `assets/profile-pro.jpg` with your new studio headshot (portrait aspect ratio recommended).
2. Run `python scripts/make_portrait.py`.
3. Commit and push the changes.

---

## 5. How the Name is Generated

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

## 6. GitHub Actions CI/CD Automation

The automated workflow in `.github/workflows/portrait.yml` runs automatically whenever:
- A new source image is committed to `assets/profile-pro.jpg`.
- Code changes occur inside `scripts/**`.
- `requirements.txt` is updated.

### Execution Flow:
1. Checks out the repository.
2. Sets up Python 3.11 with cached pip dependencies.
3. Executes `python scripts/make_portrait.py`.
4. Commits and pushes any updated SVGs back to `main` with `[skip ci]` to prevent recursive workflow triggers.
