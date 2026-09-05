#!/usr/bin/env python3
"""
scripts/generate_cards.py

Generates the complete GitSkins Cyber Terminal Dashboard design system matching test.mp4:
1. name.svg: Top terminal window with ./wordmark.sh --name and ABHAY PRATAP SINGH ASCII banner
2. ascii.svg: Hero terminal window with VISUAL.MAP (ASCII face) and SYSTEM.INFO (live telemetry)
3. assets/cards/card-profile.svg: Identity card with identicon, handle, title, pills, and radar reticle
4. assets/cards/card-highlights.svg: Highlights card with Code, dexterbeast0-cmyk, Impact
5. assets/cards/card-signal.svg: Profile Signal with 4 live metric widgets (Stars, Contributions, Repos, Followers)
6. assets/cards/card-stack.svg: Language Stack with repository-weighted progress bars
7. assets/cards/card-work.svg: PROJECTS.LIST with project cards (dexterbeast0-cmyk and toolkit)
8. assets/cards/card-activity.svg: Contribution Activity with 52x7 heatmap grid and 3 live contributions
9. assets/cards/card-contact.svg: Connect button card with GitHub @dexterbeast0-cmyk pill
"""

import collections
import math
import os
import sys
import xml.sax.saxutils as saxutils
from PIL import Image, ImageEnhance, ImageFilter

RAMP_16 = " .:-=+*cso#%8&S@"

def get_face_ascii(cols=76, char_ar=0.52):
    """
    Extracts high-resolution ASCII portrait from assets/profile-pro.jpg
    with flood-fill studio background removal.
    """
    img_path = os.path.join("assets", "profile-pro.jpg")
    if not os.path.exists(img_path):
        img_path = os.path.join("assets", "profile.jpg")
    
    raw_img = Image.open(img_path).convert("RGB")
    w, h = raw_img.size
    cx, cy = w / 2.0, h / 2.0
    pixels = raw_img.load()
    
    def is_bg(x, y):
        dist_sq = (x - cx) ** 2 + (y - cy) ** 2
        if dist_sq > (614) ** 2:
            return True
        r, g, b = pixels[x, y]
        if r > 245 and g > 245 and b > 245:
            return True
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        is_warm = (r - b > 18) and (r - g > 8)
        is_dark = lum < 80
        in_shirt = (y > 0.76 * h) and (0.28 * w < x < 0.72 * w)
        if not in_shirt and not is_warm and not is_dark and (110 <= lum <= 230):
            return True
        return False

    q = collections.deque()
    visited = set()
    for x in range(w):
        q.append((x, 0))
        q.append((x, h - 1))
    for y in range(h):
        q.append((0, y))
        q.append((w - 1, y))

    mask = Image.new("L", (w, h), 0)
    m_p = mask.load()
    for pt in q:
        visited.add(pt)

    while q:
        x, y = q.popleft()
        if is_bg(x, y):
            m_p[x, y] = 255
            for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    if is_bg(nx, ny):
                        q.append((nx, ny))

    for y in range(h):
        for x in range(w):
            if (x - cx) ** 2 + (y - cy) ** 2 > (616) ** 2:
                m_p[x, y] = 255

    # Bust crop
    crop_box = (150, 60, 1140, 1200)
    cropped = raw_img.crop(crop_box)
    crop_mask = mask.crop(crop_box)
    cw, ch = cropped.size

    gray = cropped.convert("L")
    sharp = gray.filter(ImageFilter.UnsharpMask(radius=1.5, percent=220, threshold=2))
    contrast = ImageEnhance.Contrast(sharp).enhance(1.28)

    rows = int(cols * (ch / cw) * char_ar)
    res_img = contrast.resize((cols, rows), Image.Resampling.LANCZOS)
    res_mask = crop_mask.resize((cols, rows), Image.Resampling.NEAREST)

    res_p = res_img.load()
    rm_p = res_mask.load()

    ramp = RAMP_16
    ramp_len = len(ramp)

    lines = []
    for y in range(rows):
        line = []
        for x in range(cols):
            if rm_p[x, y] > 128:
                line.append(" ")
            else:
                v = res_p[x, y]
                norm = 1.0 - (v / 255.0)
                norm = pow(max(0.0, min(1.0, norm)), 0.92)
                idx = int(norm * (ramp_len - 1))
                line.append(ramp[idx])
        lines.append("".join(line).rstrip())

    return lines


def generate_name_svg(output_path="name.svg"):
    """
    Card 1: Top terminal window with ./wordmark.sh --name and ABHAY PRATAP SINGH
    in authentic high-resolution ASCII character-density typography with continuous looping reveal.
    """
    import build_ascii_name
    build_ascii_name.build_name_svg(output_path)



def generate_hero_terminal_svg(ascii_lines, output_path="ascii.svg"):
    """
    Card 2: Hero terminal window with ./profile-scan --live.
    Two sub-panels:
      LEFT: VISUAL.MAP (ASCII face portrait)
      RIGHT: SYSTEM.INFO (Live telemetry table with dotted leaders)
    Recreates frame_00.png and frame_02.png from test.mp4.
    """
    svg_w = 960
    svg_h = 580

    sub_y = 48
    sub_h = 512
    left_w = 450
    right_w = 460
    right_x = 480

    # ASCII lines for VISUAL.MAP
    # char width ~ 5.3, line height ~ 9.0
    face_svg = []
    y_cur = sub_y + 40
    line_h = 9.2
    for line in ascii_lines[:48]:
        safe = saxutils.escape(line)
        face_svg.append(f'      <text x="36" y="{y_cur:.1f}" xml:space="preserve">{safe}</text>\n')
        y_cur += line_h

    # Telemetry data for SYSTEM.INFO
    system_fields = [
        ("Subject", "Abhay Pratap singh"),
        ("Handle", "@dexterbeast0-cmyk"),
        ("Role", "Software developer building in public"),
        ("Status", "Building | Learning | Shipping"),
        ("Languages", "Public repositories"),
        ("Repositories", "1"),
        ("Contributions", "3"),
        ("Stars", "0"),
        ("Followers", "0"),
        ("Active Days", "3"),
        ("Contact", "github.com/dexterbeast0-cmyk"),
    ]

    info_rows_svg = []
    info_start_y = sub_y + 46
    row_gap = 42
    for idx, (label, val) in enumerate(system_fields):
        ry = info_start_y + idx * row_gap
        # Dotted leader line between label and value
        dots = " " + "· " * 28
        info_rows_svg.append(f"""    <!-- Row: {label} -->
    <text x="{right_x + 24}" y="{ry}" class="sys-label">{label}</text>
    <text x="{right_x + 130}" y="{ry}" class="sys-dots">......................................</text>
    <text x="{right_x + right_w - 24}" y="{ry}" text-anchor="end" class="sys-value">{val}</text>
""")

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <defs>
    <!-- Dark Glass Chassis Gradient -->
    <linearGradient id="hero-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#05080b"/>
      <stop offset="40%" stop-color="#07151a"/>
      <stop offset="100%" stop-color="#092024"/>
    </linearGradient>

    <!-- Sub-Panel Background -->
    <linearGradient id="panel-bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#040b10"/>
      <stop offset="100%" stop-color="#061217"/>
    </linearGradient>

    <!-- Glowing Teal Border Gradient -->
    <linearGradient id="hero-border" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2c3" stop-opacity="0.35"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#00f2c3" stop-opacity="0.3"/>
    </linearGradient>

    <!-- Top Highlight Sweep -->
    <linearGradient id="top-shine-hero" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.09"/>
      <stop offset="15%" stop-color="#00f2c3" stop-opacity="0.03"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <!-- Animated Horizontal Light Sweep Beam -->
    <linearGradient id="live-beam" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#00f2c3" stop-opacity="0"/>
      <stop offset="40%" stop-color="#00f2c3" stop-opacity="0.18"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.32"/>
      <stop offset="60%" stop-color="#00f2c3" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#00f2c3" stop-opacity="0"/>
    </linearGradient>

    <!-- Soft Glow Filter -->
    <filter id="teal-glow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <style>
      .term-title {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 12px;
        fill: #00f2c3;
        font-weight: 500;
      }}
      .live-badge {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 11px;
        fill: #00f2c3;
        font-weight: 700;
        letter-spacing: 1px;
      }}
      .sub-title {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 11px;
        font-weight: 700;
        fill: #00f2c3;
        letter-spacing: 1.5px;
      }}
      .ascii-face {{
        font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Monaco, Consolas, monospace;
        font-size: 7.2px;
        fill: #c9d1d9;
        font-weight: 500;
        white-space: pre;
      }}
      .sys-label {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 12px;
        fill: #00f2c3;
        font-weight: 600;
      }}
      .sys-dots {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 12px;
        fill: #143533;
        letter-spacing: 2px;
      }}
      .sys-value {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        font-size: 12.5px;
        fill: #e6edf3;
        font-weight: 500;
      }}
      .watermark {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 9px;
        fill: #8b949e;
        opacity: 0.35;
      }}
    </style>
  </defs>

  <!-- Outer Glass Frame -->
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#hero-bg)" stroke="url(#hero-border)" stroke-width="1.2"/>
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#top-shine-hero)"/>

  <!-- Top Terminal Header -->
  <path d="M 1 16 C 1 7.7 7.7 1 16 1 L {svg_w - 16} 1 C {svg_w - 7.7} 1 {svg_w - 1} 7.7 {svg_w - 1} 16 L {svg_w - 1} 36 L 1 36 Z" fill="#04090e" stroke="#14262c" stroke-width="0.8"/>
  <line x1="1" y1="36" x2="{svg_w - 1}" y2="36" stroke="#00f2c3" stroke-width="0.8" stroke-opacity="0.3"/>

  <!-- Window Dots -->
  <circle cx="24" cy="18" r="4.5" fill="#ff5f56"/>
  <circle cx="40" cy="18" r="4.5" fill="#ffbd2e"/>
  <circle cx="56" cy="18" r="4.5" fill="#27c93f"/>

  <!-- Center Command Prompt -->
  <text x="{svg_w // 2}" y="22" text-anchor="middle" class="term-title">
    dexterbeast0-cmyk@github ~ $ ./profile-scan --live
  </text>

  <!-- Live Status Badge -->
  <circle cx="{svg_w - 65}" cy="18" r="3.5" fill="#00f2c3" filter="url(#teal-glow)"/>
  <text x="{svg_w - 54}" y="22" class="live-badge">LIVE</text>

  <!-- Left Sub-Panel: VISUAL.MAP -->
  <rect x="20" y="{sub_y}" width="{left_w}" height="{sub_h}" rx="12" fill="url(#panel-bg)" stroke="#00f2c3" stroke-width="1" stroke-opacity="0.25"/>
  <text x="36" y="{sub_y + 22}" class="sub-title">VISUAL.MAP</text>

  <!-- Right Sub-Panel: SYSTEM.INFO -->
  <rect x="{right_x}" y="{sub_y}" width="{right_w}" height="{sub_h}" rx="12" fill="url(#panel-bg)" stroke="#00f2c3" stroke-width="1" stroke-opacity="0.25"/>
  <text x="{right_x + 24}" y="{sub_y + 22}" class="sub-title">SYSTEM.INFO</text>

  <!-- ASCII Face in VISUAL.MAP -->
  <g class="ascii-face">
{''.join(face_svg)}  </g>

  <!-- Telemetry in SYSTEM.INFO -->
{''.join(info_rows_svg)}

  <!-- Animated Cyan Sweep Beam Across Panels -->
  <rect x="21" y="220" width="{svg_w - 42}" height="56" fill="url(#live-beam)" opacity="0.85" pointer-events="none">
    <animate attributeName="y" values="80; 450; 80" dur="7s" repeatCount="indefinite"/>
  </rect>

  <!-- Watermark -->
  <text x="{svg_w - 24}" y="{svg_h - 12}" text-anchor="end" class="watermark">gitskins.com</text>
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated {output_path}")


def generate_profile_identity_card(output_path="assets/cards/card-profile.svg"):
    """
    Card 3: Profile Identity Card.
    Avatar identicon, @dexterbeast0-cmyk, Abhay Pratap singh, subtitle, 3 pill buttons, radar reticle.
    Recreates frame_05.png and frame_08.png from test.mp4.
    """
    svg_w = 960
    svg_h = 210

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <defs>
    <!-- Dark Glass Base Gradient with subtle blue-purple tint on bottom-right -->
    <linearGradient id="card-prof-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#05090e"/>
      <stop offset="60%" stop-color="#07171d"/>
      <stop offset="90%" stop-color="#09222a"/>
      <stop offset="100%" stop-color="#141a38"/>
    </linearGradient>

    <!-- Glowing Teal Border Gradient -->
    <linearGradient id="prof-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f2c3" stop-opacity="0.35"/>
      <stop offset="70%" stop-color="#38bdf8" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0.3"/>
    </linearGradient>

    <!-- Top Glossy Reflection -->
    <linearGradient id="prof-shine" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="25%" stop-color="#00f2c3" stop-opacity="0.03"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <!-- Glow Filter -->
    <filter id="cyan-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <style>
      .handle-text {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 14px;
        fill: #00f2c3;
        font-weight: 600;
        letter-spacing: 0.5px;
      }}
      .name-text {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 38px;
        font-weight: 800;
        fill: #ffffff;
        letter-spacing: -0.5px;
      }}
      .sub-text {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 14.5px;
        fill: #00f2c3;
        font-weight: 400;
      }}
      .pill-text {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 12px;
        fill: #e6edf3;
        font-weight: 500;
      }}
      .watermark {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 9px;
        fill: #8b949e;
        opacity: 0.35;
      }}
    </style>
  </defs>

  <!-- Outer Glass Frame -->
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#card-prof-bg)" stroke="url(#prof-border)" stroke-width="1.2"/>
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#prof-shine)"/>

  <!-- Inner Panel -->
  <rect x="24" y="18" width="{svg_w - 48}" height="{svg_h - 36}" rx="12" fill="#040d12" stroke="#00f2c3" stroke-width="0.8" stroke-opacity="0.2"/>

  <!-- Avatar Circle with Glowing Teal Ring -->
  <g transform="translate(48, 42)">
    <circle cx="48" cy="48" r="48" fill="#06181f" stroke="#00f2c3" stroke-width="2.5" filter="url(#cyan-glow)"/>
    <circle cx="48" cy="48" r="45" fill="#f0f6fc"/>
    
    <!-- Authentic dexterbeast0-cmyk GitHub Identicon Pattern (green glyphs) -->
    <g fill="#2da44e">
      <!-- 5x5 Identicon Grid -->
      <rect x="18" y="18" width="12" height="12"/>
      <rect x="66" y="18" width="12" height="12"/>
      <rect x="18" y="30" width="12" height="12"/>
      <rect x="66" y="30" width="12" height="12"/>
      
      <rect x="18" y="42" width="60" height="12"/>
      
      <rect x="30" y="54" width="36" height="12"/>
      
      <rect x="18" y="66" width="24" height="12"/>
      <rect x="54" y="66" width="24" height="12"/>
    </g>
  </g>

  <!-- Text Hierarchy on Right of Avatar -->
  <!-- Swoosh accent line above handle -->
  <path d="M 180 44 Q 280 34 380 42" stroke="#00f2c3" stroke-width="1.2" stroke-opacity="0.45" fill="none"/>
  
  <text x="180" y="58" class="handle-text">@dexterbeast0-cmyk</text>
  <text x="180" y="98" class="name-text">Abhay Pratap singh</text>
  <text x="180" y="128" class="sub-text">Building with code on GitHub.</text>

  <!-- 3 Pill Badges -->
  <g transform="translate(180, 146)">
    <!-- Pill 1: Open Source -->
    <rect x="0" y="0" width="112" height="28" rx="14" fill="#071b22" stroke="#00f2c3" stroke-width="1" stroke-opacity="0.35"/>
    <text x="56" y="18" text-anchor="middle" class="pill-text">Open Source</text>

    <!-- Pill 2: Projects -->
    <rect x="124" y="0" width="94" height="28" rx="14" fill="#071b22" stroke="#00f2c3" stroke-width="1" stroke-opacity="0.35"/>
    <text x="171" y="18" text-anchor="middle" class="pill-text">Projects</text>

    <!-- Pill 3: Systems -->
    <rect x="230" y="0" width="94" height="28" rx="14" fill="#071b22" stroke="#00f2c3" stroke-width="1" stroke-opacity="0.35"/>
    <text x="277" y="18" text-anchor="middle" class="pill-text">Systems</text>
  </g>

  <!-- Radar Reticle / Concentric Circle Widget on Right -->
  <g transform="translate({svg_w - 140}, 105)" stroke="#00f2c3" stroke-width="0.8" opacity="0.3" fill="none">
    <circle cx="0" cy="0" r="42"/>
    <circle cx="0" cy="0" r="26"/>
    <circle cx="0" cy="0" r="10"/>
    <circle cx="-16" cy="-8" r="3" fill="#00f2c3" opacity="0.8"/>
  </g>

  <!-- Watermark -->
  <text x="{svg_w - 24}" y="{svg_h - 12}" text-anchor="end" class="watermark">gitskins.com</text>
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated {output_path}")


def generate_highlights_card(output_path="assets/cards/card-highlights.svg"):
    """
    Card 4: HIGHLIGHTS Card.
    3 sub-cards: Code (1 public repositories), dexterbeast0-cmyk (Featured project), Impact (0 stars · 3 active days).
    Recreates frame_08.png from test.mp4.
    """
    svg_w = 960
    svg_h = 160

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <defs>
    <!-- Dark Glass Base Gradient -->
    <linearGradient id="hl-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#05080c"/>
      <stop offset="50%" stop-color="#08181f"/>
      <stop offset="100%" stop-color="#0b242a"/>
    </linearGradient>

    <!-- Sub-card background -->
    <linearGradient id="sub-card-bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#051217"/>
      <stop offset="100%" stop-color="#071920"/>
    </linearGradient>

    <!-- Glowing Teal Border -->
    <linearGradient id="hl-border" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2c3" stop-opacity="0.3"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#00f2c3" stop-opacity="0.3"/>
    </linearGradient>

    <linearGradient id="hl-shine" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="30%" stop-color="#00f2c3" stop-opacity="0.02"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <style>
      .hl-header {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 11px;
        font-weight: 700;
        fill: #00f2c3;
        letter-spacing: 2.5px;
      }}
      .tile-title {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 16px;
        font-weight: 700;
        fill: #ffffff;
      }}
      .tile-sub {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 12px;
        fill: #8b949e;
      }}
      .watermark {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 9px;
        fill: #8b949e;
        opacity: 0.35;
      }}
    </style>
  </defs>

  <!-- Chassis -->
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#hl-bg)" stroke="url(#hl-border)" stroke-width="1.2"/>
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#hl-shine)"/>

  <!-- Header -->
  <text x="32" y="32" class="hl-header">H I G H L I G H T S</text>

  <!-- 3 Sub-Cards -->
  <g transform="translate(30, 48)">
    <!-- Sub-card 1: Code -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="286" height="88" rx="10" fill="url(#sub-card-bg)" stroke="#00f2c3" stroke-width="0.8" stroke-opacity="0.25"/>
      <!-- Accent bar on left: Green -->
      <rect x="2" y="22" width="3.5" height="44" rx="1.5" fill="#39d353"/>
      <text x="24" y="38" class="tile-title">Code</text>
      <text x="24" y="62" class="tile-sub">1 public repositories</text>
    </g>

    <!-- Sub-card 2: dexterbeast0-cmyk -->
    <g transform="translate(306, 0)">
      <rect x="0" y="0" width="286" height="88" rx="10" fill="url(#sub-card-bg)" stroke="#00f2c3" stroke-width="0.8" stroke-opacity="0.25"/>
      <!-- Accent bar on left: Cyan -->
      <rect x="2" y="22" width="3.5" height="44" rx="1.5" fill="#00f2c3"/>
      <text x="24" y="38" class="tile-title">dexterbeast0-cmyk</text>
      <text x="24" y="62" class="tile-sub">Featured project</text>
    </g>

    <!-- Sub-card 3: Impact -->
    <g transform="translate(612, 0)">
      <rect x="0" y="0" width="286" height="88" rx="10" fill="url(#sub-card-bg)" stroke="#00f2c3" stroke-width="0.8" stroke-opacity="0.25"/>
      <!-- Accent bar on left: Blue -->
      <rect x="2" y="22" width="3.5" height="44" rx="1.5" fill="#58a6ff"/>
      <text x="24" y="38" class="tile-title">Impact</text>
      <text x="24" y="62" class="tile-sub">0 stars · 3 active days</text>
    </g>
  </g>

  <!-- Watermark -->
  <text x="{svg_w - 24}" y="{svg_h - 12}" text-anchor="end" class="watermark">gitskins.com</text>
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated {output_path}")


def generate_signal_card(output_path="assets/cards/card-signal.svg"):
    """
    Card 5: Profile Signal Card.
    4 metric widgets: Stars (0), Contributions (3), Repos (1), Followers (0).
    Recreates frame_10.png from test.mp4.
    """
    svg_w = 960
    svg_h = 210

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <defs>
    <!-- Dark Glass Base Gradient with purple/blue lower edge -->
    <linearGradient id="sig-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#05080c"/>
      <stop offset="50%" stop-color="#07181e"/>
      <stop offset="85%" stop-color="#092228"/>
      <stop offset="100%" stop-color="#121834"/>
    </linearGradient>

    <!-- Sub-widget background -->
    <linearGradient id="sig-widget-bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#051217"/>
      <stop offset="100%" stop-color="#071920"/>
    </linearGradient>

    <!-- Border Gradient -->
    <linearGradient id="sig-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f2c3" stop-opacity="0.35"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0.3"/>
    </linearGradient>

    <linearGradient id="sig-shine" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="25%" stop-color="#00f2c3" stop-opacity="0.03"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <filter id="sig-glow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <style>
      .sig-title {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 24px;
        font-weight: 800;
        fill: #ffffff;
      }}
      .sig-sub {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 12.5px;
        fill: #00f2c3;
        font-weight: 500;
      }}
      .widget-label {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 11.5px;
        fill: #8b949e;
        font-weight: 600;
      }}
      .widget-val {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 36px;
        font-weight: 800;
      }}
      .watermark {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 9px;
        fill: #8b949e;
        opacity: 0.35;
      }}
    </style>
  </defs>

  <!-- Chassis -->
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#sig-bg)" stroke="url(#sig-border)" stroke-width="1.2"/>
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#sig-shine)"/>

  <!-- Top Title Area -->
  <text x="32" y="44" class="sig-title">Profile Signal</text>
  <text x="32" y="66" class="sig-sub">Live GitHub stats styled by GitSkins</text>

  <!-- Top Right Indicator Dot -->
  <circle cx="{svg_w - 40}" cy="38" r="4.5" fill="#00f2c3" filter="url(#sig-glow)"/>

  <!-- 4 Metric Widgets -->
  <g transform="translate(30, 84)">
    <!-- Widget 1: Stars -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="212" height="96" rx="10" fill="url(#sig-widget-bg)" stroke="#00f2c3" stroke-width="0.8" stroke-opacity="0.25"/>
      <text x="20" y="28" class="widget-label">Stars</text>
      <text x="20" y="66" class="widget-val" fill="#00f2c3">0</text>
      <!-- Mini Progress Line -->
      <rect x="20" y="76" width="172" height="3" rx="1.5" fill="#12252c"/>
      <rect x="20" y="76" width="18" height="3" rx="1.5" fill="#00f2c3"/>
    </g>

    <!-- Widget 2: Contributions -->
    <g transform="translate(228, 0)">
      <rect x="0" y="0" width="212" height="96" rx="10" fill="url(#sig-widget-bg)" stroke="#00f2c3" stroke-width="0.8" stroke-opacity="0.25"/>
      <text x="20" y="28" class="widget-label">Contributions</text>
      <text x="20" y="66" class="widget-val" fill="#c084fc">3</text>
      <!-- Mini Progress Line: Purple -->
      <rect x="20" y="76" width="172" height="3" rx="1.5" fill="#12252c"/>
      <rect x="20" y="76" width="145" height="3" rx="1.5" fill="#a855f7"/>
    </g>

    <!-- Widget 3: Repos -->
    <g transform="translate(456, 0)">
      <rect x="0" y="0" width="212" height="96" rx="10" fill="url(#sig-widget-bg)" stroke="#00f2c3" stroke-width="0.8" stroke-opacity="0.25"/>
      <text x="20" y="28" class="widget-label">Repos</text>
      <text x="20" y="66" class="widget-val" fill="#60a5fa">1</text>
      <!-- Mini Progress Line: Blue -->
      <rect x="20" y="76" width="172" height="3" rx="1.5" fill="#12252c"/>
      <rect x="20" y="76" width="48" height="3" rx="1.5" fill="#3b82f6"/>
    </g>

    <!-- Widget 4: Followers -->
    <g transform="translate(684, 0)">
      <rect x="0" y="0" width="212" height="96" rx="10" fill="url(#sig-widget-bg)" stroke="#00f2c3" stroke-width="0.8" stroke-opacity="0.25"/>
      <text x="20" y="28" class="widget-label">Followers</text>
      <text x="20" y="66" class="widget-val" fill="#00f2c3">0</text>
      <!-- Mini Progress Line -->
      <rect x="20" y="76" width="172" height="3" rx="1.5" fill="#12252c"/>
      <rect x="20" y="76" width="18" height="3" rx="1.5" fill="#00f2c3"/>
    </g>
  </g>

  <!-- Watermark -->
  <text x="{svg_w - 24}" y="{svg_h - 12}" text-anchor="end" class="watermark">gitskins.com</text>
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated {output_path}")


def generate_stack_card(output_path="assets/cards/card-stack.svg"):
    """
    Card 6: Language Stack Card.
    Repository-weighted technologies: Python (52%), SVG/Vector (33%), GitHub Actions (15%).
    Recreates frame_10.png and frame_12.png from test.mp4.
    """
    svg_w = 960
    svg_h = 220

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <defs>
    <!-- Dark Glass Base Gradient -->
    <linearGradient id="stack-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#05080c"/>
      <stop offset="50%" stop-color="#07181e"/>
      <stop offset="100%" stop-color="#0a2228"/>
    </linearGradient>

    <!-- Border Gradient -->
    <linearGradient id="stack-border" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2c3" stop-opacity="0.35"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#00f2c3" stop-opacity="0.3"/>
    </linearGradient>

    <linearGradient id="stack-shine" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="25%" stop-color="#00f2c3" stop-opacity="0.03"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <style>
      .stack-title {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 24px;
        font-weight: 800;
        fill: #ffffff;
      }}
      .stack-sub {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 12.5px;
        fill: #00f2c3;
        font-weight: 500;
      }}
      .stack-scan {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 12px;
        fill: #00f2c3;
        font-weight: 600;
      }}
      .lang-name {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 14px;
        font-weight: 600;
        fill: #ffffff;
      }}
      .lang-pct {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 13px;
        font-weight: 600;
        fill: #e6edf3;
      }}
      .watermark {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 9px;
        fill: #8b949e;
        opacity: 0.35;
      }}
    </style>
  </defs>

  <!-- Chassis -->
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#stack-bg)" stroke="url(#stack-border)" stroke-width="1.2"/>
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#stack-shine)"/>

  <!-- Header -->
  <text x="32" y="44" class="stack-title">Language Stack</text>
  <text x="32" y="66" class="stack-sub">Repository-weighted technologies</text>

  <!-- Top Right Scanner Command -->
  <text x="{svg_w - 36}" y="44" text-anchor="end" class="stack-scan">&gt; stack.scan  _</text>

  <!-- Stack Bars -->
  <g transform="translate(32, 95)">
    <!-- Row 1: Python -->
    <g transform="translate(0, 0)">
      <circle cx="6" cy="11" r="4.5" fill="#00f2c3"/>
      <text x="22" y="16" class="lang-name">Python</text>
      <text x="230" y="16" class="lang-pct">52%</text>
      <!-- Progress Bar Track -->
      <rect x="280" y="7" width="600" height="9" rx="4.5" fill="#0b1e24"/>
      <!-- Filled Bar -->
      <rect x="280" y="7" width="312" height="9" rx="4.5" fill="#00f2c3"/>
    </g>

    <!-- Row 2: SVG / Vector -->
    <g transform="translate(0, 36)">
      <circle cx="6" cy="11" r="4.5" fill="#38bdf8"/>
      <text x="22" y="16" class="lang-name">SVG / Vector</text>
      <text x="230" y="16" class="lang-pct">33%</text>
      <!-- Progress Bar Track -->
      <rect x="280" y="7" width="600" height="9" rx="4.5" fill="#0b1e24"/>
      <!-- Filled Bar -->
      <rect x="280" y="7" width="198" height="9" rx="4.5" fill="#38bdf8"/>
    </g>

    <!-- Row 3: YAML / CI-CD -->
    <g transform="translate(0, 72)">
      <circle cx="6" cy="11" r="4.5" fill="#34d399"/>
      <text x="22" y="16" class="lang-name">YAML / Actions</text>
      <text x="230" y="16" class="lang-pct">15%</text>
      <!-- Progress Bar Track -->
      <rect x="280" y="7" width="600" height="9" rx="4.5" fill="#0b1e24"/>
      <!-- Filled Bar -->
      <rect x="280" y="7" width="90" height="9" rx="4.5" fill="#34d399"/>
    </g>
  </g>

  <!-- Watermark -->
  <text x="{svg_w - 24}" y="{svg_h - 12}" text-anchor="end" class="watermark">gitskins.com</text>
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated {output_path}")


def generate_work_card(output_path="assets/cards/card-work.svg"):
    """
    Card 7: PROJECTS.LIST Card.
    PROJECTS.LIST ./projects.sh --all 2 pinned.
    Two project sub-cards: dexterbeast0-cmyk and toolkit.
    Recreates frame_12.png from test.mp4.
    """
    svg_w = 960
    svg_h = 260

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <defs>
    <!-- Dark Glass Base -->
    <linearGradient id="work-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#05080c"/>
      <stop offset="50%" stop-color="#07181e"/>
      <stop offset="100%" stop-color="#0a2228"/>
    </linearGradient>

    <!-- Sub-card background -->
    <linearGradient id="work-card-bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#040e13"/>
      <stop offset="100%" stop-color="#06161c"/>
    </linearGradient>

    <!-- Border Gradient -->
    <linearGradient id="work-border" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2c3" stop-opacity="0.35"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#00f2c3" stop-opacity="0.3"/>
    </linearGradient>

    <linearGradient id="work-shine" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="25%" stop-color="#00f2c3" stop-opacity="0.03"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <filter id="donut-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <style>
      .work-header {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 11px;
        font-weight: 700;
        fill: #00f2c3;
        letter-spacing: 1.5px;
      }}
      .work-pinned {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 11px;
        fill: #8b949e;
      }}
      .proj-title {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 16px;
        font-weight: 700;
        fill: #ffffff;
      }}
      .proj-desc {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 12.5px;
        fill: #00f2c3;
        font-weight: 400;
      }}
      .proj-pill {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 11px;
        fill: #00f2c3;
      }}
      .proj-meta {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 11px;
        fill: #8b949e;
      }}
      .donut-text {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 12px;
        font-weight: 800;
        fill: #ffffff;
      }}
      .watermark {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 9px;
        fill: #8b949e;
        opacity: 0.35;
      }}
    </style>
  </defs>

  <!-- Chassis -->
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#work-bg)" stroke="url(#work-border)" stroke-width="1.2"/>
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#work-shine)"/>

  <!-- Top Header Line -->
  <text x="32" y="32" class="work-header">PROJECTS.LIST &#160;&#160;&#160; <tspan fill="#8b949e">./projects.sh --all</tspan></text>
  <text x="{svg_w - 32}" y="32" text-anchor="end" class="work-pinned">2 pinned</text>
  <line x1="32" y1="42" x2="{svg_w - 32}" y2="42" stroke="#00f2c3" stroke-width="0.8" stroke-opacity="0.2"/>

  <!-- Two Project Sub-Cards -->
  <g transform="translate(30, 56)">
    <!-- Sub-Card 1: dexterbeast0-cmyk -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="436" height="176" rx="10" fill="url(#work-card-bg)" stroke="#00f2c3" stroke-width="0.8" stroke-opacity="0.25"/>
      <!-- Top mini bar inside card -->
      <path d="M 0 10 C 0 4.5 4.5 0 10 0 L 426 0 C 431.5 0 436 4.5 436 10 L 436 28 L 0 28 Z" fill="#061217"/>
      <line x1="0" y1="28" x2="436" y2="28" stroke="#00f2c3" stroke-width="0.6" stroke-opacity="0.2"/>
      <circle cx="16" cy="14" r="3" fill="#00f2c3"/>
      <text x="26" y="18" font-family="ui-monospace, monospace" font-size="11" fill="#8b949e">awesome-project</text>
      <circle cx="420" cy="14" r="3.5" fill="#39d353"/>

      <!-- Content -->
      <text x="20" y="56" class="proj-title">awesome-project &#160;<tspan fill="#00f2c3">_</tspan></text>
      <text x="20" y="78" class="proj-desc">A standout open-source project.</text>

      <!-- Donut Progress Chart on Right: 80% -->
      <g transform="translate(380, 84)">
        <circle cx="0" cy="0" r="28" fill="none" stroke="#0b242e" stroke-width="7"/>
        <!-- 80% of 2*pi*28 = 175.9. Circumference = 175.9. 80% stroke = 140.7, dasharray = 140.7 35.2 -->
        <circle cx="0" cy="0" r="28" fill="none" stroke="#38bdf8" stroke-width="7" stroke-dasharray="140.7 35.2" stroke-dashoffset="44" stroke-linecap="round" filter="url(#donut-glow)"/>
        <text x="0" y="4" text-anchor="middle" class="donut-text">80%</text>
      </g>

      <!-- Pill Tag -->
      <rect x="20" y="104" width="88" height="22" rx="11" fill="#062227" stroke="#00f2c3" stroke-width="0.8" stroke-opacity="0.35"/>
      <text x="64" y="119" text-anchor="middle" class="proj-pill">open-source</text>

      <!-- Footer Meta -->
      <text x="20" y="152" class="proj-meta">★ 0 &#160;&#160; updated just now</text>
    </g>

    <!-- Sub-Card 2: toolkit -->
    <g transform="translate(464, 0)">
      <rect x="0" y="0" width="436" height="176" rx="10" fill="url(#work-card-bg)" stroke="#00f2c3" stroke-width="0.8" stroke-opacity="0.25"/>
      <!-- Top mini bar -->
      <path d="M 0 10 C 0 4.5 4.5 0 10 0 L 426 0 C 431.5 0 436 4.5 436 10 L 436 28 L 0 28 Z" fill="#061217"/>
      <line x1="0" y1="28" x2="436" y2="28" stroke="#00f2c3" stroke-width="0.6" stroke-opacity="0.2"/>
      <circle cx="16" cy="14" r="3" fill="#00f2c3"/>
      <text x="26" y="18" font-family="ui-monospace, monospace" font-size="11" fill="#8b949e">toolkit</text>
      <circle cx="420" cy="14" r="3.5" fill="#39d353"/>

      <!-- Content -->
      <text x="20" y="56" class="proj-title">toolkit &#160;<tspan fill="#00f2c3">_</tspan></text>
      <text x="20" y="78" class="proj-desc">Reusable building blocks and</text>
      <text x="20" y="96" class="proj-desc">utilities.</text>

      <!-- Footer Meta -->
      <text x="20" y="152" class="proj-meta">★ 0 &#160;&#160; updated n/a</text>
    </g>
  </g>

  <!-- Watermark -->
  <text x="{svg_w - 24}" y="{svg_h - 12}" text-anchor="end" class="watermark">gitskins.com</text>
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated {output_path}")


def generate_activity_card(output_path="assets/cards/card-activity.svg"):
    """
    Card 8: Contribution Activity Card.
    52x7 heatmap grid with 3 live contributions glowing teal.
    Recreates frame_12.png and frame_14.png from test.mp4.
    """
    svg_w = 960
    svg_h = 210

    # Build 52 columns x 7 rows heatmap grid
    # cell size = 12, gap = 4
    # grid width = 52 * 16 = 832
    # grid height = 7 * 16 = 112
    # x offset = (960 - 832) / 2 = 64
    grid_svg = []
    x_start = 54
    y_start = 82
    cell_size = 12
    gap = 4

    # 3 genuine contributions in the past year:
    # In frame_12.png, there is 1 active block around week 6, and 2 active blocks at the very end of the year!
    active_cells = {(6, 2), (51, 5), (51, 6)}

    for col in range(52):
        for row in range(7):
            cx = x_start + col * (cell_size + gap)
            cy = y_start + row * (cell_size + gap)
            if (col, row) in active_cells:
                grid_svg.append(
                    f'    <rect x="{cx}" y="{cy}" width="{cell_size}" height="{cell_size}" rx="2.5" fill="#00f2c3" filter="url(#act-glow)"/>\n'
                )
            else:
                grid_svg.append(
                    f'    <rect x="{cx}" y="{cy}" width="{cell_size}" height="{cell_size}" rx="2.5" fill="#08181e" stroke="#0e2830" stroke-width="0.7"/>\n'
                )

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <defs>
    <!-- Dark Glass Base -->
    <linearGradient id="act-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#05080c"/>
      <stop offset="50%" stop-color="#07181e"/>
      <stop offset="100%" stop-color="#0a2228"/>
    </linearGradient>

    <!-- Border Gradient -->
    <linearGradient id="act-border" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2c3" stop-opacity="0.35"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#00f2c3" stop-opacity="0.3"/>
    </linearGradient>

    <linearGradient id="act-shine" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="25%" stop-color="#00f2c3" stop-opacity="0.03"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <filter id="act-glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <style>
      .act-title {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 24px;
        font-weight: 800;
        fill: #ffffff;
      }}
      .act-sub {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 12.5px;
        fill: #00f2c3;
        font-weight: 500;
      }}
      .legend-text {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 11px;
        fill: #8b949e;
      }}
      .watermark {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 9px;
        fill: #8b949e;
        opacity: 0.35;
      }}
    </style>
  </defs>

  <!-- Chassis -->
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#act-bg)" stroke="url(#act-border)" stroke-width="1.2"/>
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#act-shine)"/>

  <!-- Inner Recessed Panel -->
  <rect x="24" y="18" width="{svg_w - 48}" height="{svg_h - 36}" rx="12" fill="#040d12" stroke="#00f2c3" stroke-width="0.8" stroke-opacity="0.2"/>

  <!-- Header -->
  <text x="44" y="46" class="act-title">Contribution Activity</text>
  <text x="44" y="68" class="act-sub">3 contributions in the last year</text>

  <!-- Legend on Top Right -->
  <g transform="translate({svg_w - 180}, 36)">
    <text x="0" y="11" class="legend-text">Less</text>
    <rect x="30" y="0" width="11" height="11" rx="2" fill="#08181e" stroke="#0e2830" stroke-width="0.5"/>
    <rect x="45" y="0" width="11" height="11" rx="2" fill="#0d3835"/>
    <rect x="60" y="0" width="11" height="11" rx="2" fill="#00a884"/>
    <rect x="75" y="0" width="11" height="11" rx="2" fill="#00f2c3"/>
    <text x="94" y="11" class="legend-text">More</text>
  </g>

  <!-- 52 x 7 Heatmap Grid -->
  <g>
{''.join(grid_svg)}  </g>

  <!-- Watermark -->
  <text x="{svg_w - 24}" y="{svg_h - 12}" text-anchor="end" class="watermark">gitskins.com</text>
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated {output_path}")


def generate_contact_card(output_path="assets/cards/card-contact.svg"):
    """
    Card 9: Connect / GitHub Badge Card.
    Centered glass pill button with GitHub logo, GitHub header, @dexterbeast0-cmyk.
    Recreates frame_14.png from test.mp4.
    """
    svg_w = 960
    svg_h = 120

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <defs>
    <!-- Dark Glass Base Gradient with purple/blue edge tint -->
    <linearGradient id="conn-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#05080c"/>
      <stop offset="50%" stop-color="#07181e"/>
      <stop offset="85%" stop-color="#092228"/>
      <stop offset="100%" stop-color="#141a3a"/>
    </linearGradient>

    <!-- Border Gradient -->
    <linearGradient id="conn-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f2c3" stop-opacity="0.35"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0.35"/>
    </linearGradient>

    <linearGradient id="conn-shine" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="30%" stop-color="#00f2c3" stop-opacity="0.03"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <filter id="pill-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <style>
      .pill-lbl {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 11px;
        font-weight: 700;
        fill: #00f2c3;
      }}
      .pill-val {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 13.5px;
        font-weight: 800;
        fill: #ffffff;
      }}
      .watermark {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 9px;
        fill: #8b949e;
        opacity: 0.35;
      }}
    </style>
  </defs>

  <!-- Chassis -->
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#conn-bg)" stroke="url(#conn-border)" stroke-width="1.2"/>
  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" rx="16" fill="url(#conn-shine)"/>

  <!-- Centered Glass Pill Button -->
  <g transform="translate({(svg_w - 220) // 2}, 34)">
    <rect x="0" y="0" width="220" height="52" rx="26" fill="#041217" stroke="#00f2c3" stroke-width="1.2" stroke-opacity="0.5" filter="url(#pill-glow)"/>
    
    <!-- GitHub Octocat Icon in Circle -->
    <g transform="translate(18, 12)">
      <circle cx="14" cy="14" r="14" fill="#09222a"/>
      <path d="M14 4C8.48 4 4 8.48 4 14c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.1-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V23c0 .27.16.59.67.5C21.14 22.16 24 18.42 24 14c0-5.52-4.48-10-10-10z" fill="#ffffff"/>
    </g>

    <!-- Labels -->
    <text x="56" y="24" class="pill-lbl">GitHub</text>
    <text x="56" y="40" class="pill-val">@dexterbeast0-cmyk</text>
  </g>

  <!-- Watermark -->
  <text x="{svg_w - 24}" y="{svg_h - 12}" text-anchor="end" class="watermark">gitskins.com</text>
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated {output_path}")


def main():
    os.makedirs("assets/cards", exist_ok=True)

    print("Generating ASCII face portrait lines...")
    face_lines = get_face_ascii(cols=76, char_ar=0.52)

    print("1. Generating name.svg (Top Terminal Wordmark)...")
    generate_name_svg("name.svg")

    print("2. Generating ascii.svg (Hero Terminal Window)...")
    generate_hero_terminal_svg(face_lines, "ascii.svg")

    print("3. Generating assets/cards/card-profile.svg (Identity Card)...")
    generate_profile_identity_card("assets/cards/card-profile.svg")

    print("4. Generating assets/cards/card-highlights.svg (Highlights Card)...")
    generate_highlights_card("assets/cards/card-highlights.svg")

    print("5. Generating assets/cards/card-signal.svg (Profile Signal Card)...")
    generate_signal_card("assets/cards/card-signal.svg")

    print("6. Generating assets/cards/card-stack.svg (Language Stack Card)...")
    generate_stack_card("assets/cards/card-stack.svg")

    print("7. Generating assets/cards/card-work.svg (PROJECTS.LIST Card)...")
    generate_work_card("assets/cards/card-work.svg")

    print("8. Generating assets/cards/card-activity.svg (Contribution Activity Card)...")
    generate_activity_card("assets/cards/card-activity.svg")

    print("9. Generating assets/cards/card-contact.svg (Connect Button Card)...")
    generate_contact_card("assets/cards/card-contact.svg")

    print("\nAll cards generated successfully!")


if __name__ == "__main__":
    main()
