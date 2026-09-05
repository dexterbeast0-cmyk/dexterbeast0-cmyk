#!/usr/bin/env python3
"""
scripts/build_ascii_name.py

Generates name.svg strictly matching the user's requirements:
- Exact full name: "ABHAY PRATAP SINGH" on ONE SINGLE LINE
- Authentic high-resolution ASCII character-density typography matching ascii.svg
- Soft light grey base palette (#C9D1D9 / #8B949E) with crisp reveal (#F0F6FC)
- Cyber teal/cyan (#00F2C3) reserved exclusively for the scanline, corner brackets, and reflection
- Letter-by-letter reveal:
    * Starts dim/hidden
    * Scanline travels LEFT -> RIGHT over ~3.0s
    * As the scan passes each letter, that letter is progressively revealed:
      A -> AB -> ABH -> ABHA -> ABHAY -> ABHAY P -> ABHAY PR ... -> ABHAY PRATAP SINGH
- Full name holds in brilliant crisp soft-grey/white (~0.5s)
- Glossy cyan/teal specular reflection streak sweeps across letters (~0.8s)
- Smooth fade/dim down to dim/hidden (~0.7s)
- Immediate seamless reset and loop FOREVER
- Zero clipping: Wide responsive layout with 50px margins inside brackets, no cutoffs.
- Static fallback: Complete "ABHAY PRATAP SINGH" rendered in crisp soft grey.
"""

import os
import xml.sax.saxutils as saxutils

# 9-row tall high-resolution ASCII letterforms (12 characters wide each)
LETTER_DEFS = {
    'A': [
        '   .8888.   ',
        '  :888888:  ',
        " .88'  '88. ",
        ' 888    888 ',
        ' 8888888888 ',
        ' 8888888888 ',
        ' 888    888 ',
        ' 888    888 ',
        ':888:  :888:',
    ],
    'B': [
        '88888888:   ',
        '8888888888. ',
        "888'    '888",
        "8888888888' ",
        '8888888888. ',
        "888'    '888",
        '888      888',
        "88888888888'",
        ":88888888'  ",
    ],
    'H': [
        '888:    :888',
        '8888    8888',
        '8888    8888',
        '888888888888',
        '888888888888',
        '8888    8888',
        '8888    8888',
        '8888    8888',
        ':888:  :888:',
    ],
    'Y': [
        '888:    :888',
        ':888:  :888:',
        " '88888888' ",
        "   '8888'   ",
        '    8888    ',
        '    8888    ',
        '    8888    ',
        '    8888    ',
        '   :8888:   ',
    ],
    'P': [
        '88888888:   ',
        '8888888888. ',
        "888'    '888",
        '888.    .888',
        "8888888888' ",
        "888'        ",
        '888         ',
        '888         ',
        ':888:       ',
    ],
    'R': [
        '88888888:   ',
        '8888888888. ',
        "888'    '888",
        "8888888888' ",
        '8888888888. ',
        "888'   '888.",
        '888     888 ',
        '888:   :888:',
        ':888:  :888:',
    ],
    'T': [
        '888888888888',
        '888888888888',
        "   '8888'   ",
        '    8888    ',
        '    8888    ',
        '    8888    ',
        '    8888    ',
        '    8888    ',
        '   :8888:   ',
    ],
    'S': [
        ' .::8888::. ',
        ':8888888888:',
        "888'    '888",
        " '888888:.  ",
        "   '::88888:",
        "888'    '888",
        '888.    .888',
        ':8888888888:',
        " '::8888::' ",
    ],
    'I': [
        '  88888888  ',
        '  88888888  ',
        '    8888    ',
        '    8888    ',
        '    8888    ',
        '    8888    ',
        '    8888    ',
        '  88888888  ',
        '  88888888  ',
    ],
    'N': [
        '888:    :888',
        '8888:   :888',
        '88888.  :888',
        "888'88. :888",
        "888 '88.:888",
        "888  '888888",
        "888   '88888",
        "888    '8888",
        ':88:    :88:',
    ],
    'G': [
        ' .::8888::. ',
        ':8888888888:',
        "888'    '888",
        '888         ',
        '888    :8888',
        '888    :8888',
        '888.    .888',
        ':8888888888:',
        " '::8888::' ",
    ],
}

def generate_ascii_matrix():
    words = ["ABHAY", "PRATAP", "SINGH"]
    rows = ["" for _ in range(9)]
    
    char_gap = " "
    word_gap = "   "
    
    for w_idx, word in enumerate(words):
        for c_idx, char in enumerate(word):
            p = LETTER_DEFS[char]
            for r in range(9):
                rows[r] += p[r]
                if c_idx < len(word) - 1:
                    rows[r] += char_gap
        if w_idx < len(words) - 1:
            for r in range(9):
                rows[r] += word_gap
                
    return rows

def build_name_svg(output_path="name.svg"):
    matrix_rows = generate_ascii_matrix()
    total_cols = len(matrix_rows[0])
    
    svg_w = 960
    svg_h = 180
    dur = 5.0  # seconds
    
    # 211 cols * 4.08px = 860.9px
    # With start at x=50, text spans x=50.0 to x=910.9
    # Left margin: 50px | Right margin: 49px (inside corner brackets at 28 and 932)
    x_start = 50.0
    y_start = 68.0
    line_h = 10.4
    
    text_lines_dim = []
    text_lines_bright = []
    
    for i, row in enumerate(matrix_rows):
        safe = saxutils.escape(row)
        y = y_start + i * line_h
        text_lines_dim.append(f'    <text x="{x_start}" y="{y:.1f}" xml:space="preserve">{safe}</text>\n')
        text_lines_bright.append(f'    <text x="{x_start}" y="{y:.1f}" xml:space="preserve">{safe}</text>\n')

    dim_block = "".join(text_lines_dim)
    bright_block = "".join(text_lines_bright)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <defs>
    <!-- Dark Glass Chassis Gradient -->
    <linearGradient id="card-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#05080c"/>
      <stop offset="50%" stop-color="#07151a"/>
      <stop offset="100%" stop-color="#092024"/>
    </linearGradient>

    <!-- Glowing Teal Border Gradient -->
    <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2c3" stop-opacity="0.35"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#00f2c3" stop-opacity="0.3"/>
    </linearGradient>

    <!-- Top Glossy Reflection -->
    <linearGradient id="top-shine" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="25%" stop-color="#00f2c3" stop-opacity="0.03"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <!-- Brighter Reveal Highlight (#F0F6FC) for Active Revealed State -->
    <linearGradient id="bright-white-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="50%" stop-color="#f0f6fc"/>
      <stop offset="100%" stop-color="#dce3ea"/>
    </linearGradient>

    <!-- Glossy Cyan/Green Specular Highlight Flare (Moving Reflection Sweep) -->
    <linearGradient id="specular-streak" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2c3" stop-opacity="0"/>
      <stop offset="25%" stop-color="#00f2c3" stop-opacity="0.25"/>
      <stop offset="47%" stop-color="#38bdf8" stop-opacity="0.85"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="1.0"/>
      <stop offset="53%" stop-color="#00f2c3" stop-opacity="0.85"/>
      <stop offset="75%" stop-color="#00f2c3" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#00f2c3" stop-opacity="0"/>
    </linearGradient>

    <!-- Luminous Vertical Scanline Gradient (Laser Glow) -->
    <linearGradient id="scanline-glow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2c3" stop-opacity="0"/>
      <stop offset="30%" stop-color="#00f2c3" stop-opacity="0.45"/>
      <stop offset="46%" stop-color="#38bdf8" stop-opacity="0.95"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="1.0"/>
      <stop offset="54%" stop-color="#00f2c3" stop-opacity="0.95"/>
      <stop offset="70%" stop-color="#00f2c3" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#00f2c3" stop-opacity="0"/>
    </linearGradient>

    <!-- Soft Filter for Revealed Text -->
    <filter id="text-soft-glow" x="-5%" y="-10%" width="110%" height="120%">
      <feGaussianBlur stdDeviation="0.6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Flare Filter for Scanline and Reflection -->
    <filter id="scan-flare" x="-60%" y="-20%" width="220%" height="140%">
      <feGaussianBlur stdDeviation="3.0" result="b1"/>
      <feGaussianBlur stdDeviation="1.0" result="b2"/>
      <feMerge>
        <feMergeNode in="b1"/>
        <feMergeNode in="b2"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Progressive Reveal Mask: Expands from LEFT (x=46) to RIGHT across entire wordmark -->
    <!-- Static default width="872" ensures static fallback renders 100% of the name -->
    <mask id="ascii-reveal-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="{svg_w}" height="{svg_h}">
      <rect x="0" y="0" width="{svg_w}" height="{svg_h}" fill="#000000"/>
      <rect x="46" y="42" width="872" height="125" fill="#ffffff">
        <animate attributeName="width"
                 values="0; 872; 872; 872; 0"
                 keyTimes="0; 0.60; 0.70; 0.86; 1"
                 dur="{dur}s"
                 repeatCount="indefinite"
                 calcMode="linear"/>
      </rect>
    </mask>

    <style>
      .term-cmd {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 11px;
        fill: #8b949e;
      }}
      .online-badge {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 10.5px;
        font-weight: 700;
        fill: #00f2c3;
        letter-spacing: 0.8px;
      }}
      .ascii-base {{
        font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Monaco, Consolas, "Liberation Mono", monospace;
        font-size: 6.8px;
        font-weight: 700;
        letter-spacing: 0.0px;
        white-space: pre;
      }}
      .dim-ghost {{
        fill: #8b949e;
        opacity: 0.05;
      }}
      .bright-grey {{
        fill: url(#bright-white-grad);
      }}
    </style>
  </defs>

  <!-- Glass Chassis -->
  <rect x="1" y="1" width="958" height="178" rx="12" fill="url(#card-bg)" stroke="url(#border-grad)" stroke-width="1.2"/>
  <rect x="1" y="1" width="958" height="178" rx="12" fill="url(#top-shine)"/>

  <!-- Top Terminal Bar -->
  <path d="M 1 12 C 1 5.9 5.9 1 12 1 L 948 1 C 954.1 1 959 5.9 959 12 L 959 34 L 1 34 Z" fill="#04090e" stroke="#14262c" stroke-width="0.8"/>
  <line x1="1" y1="34" x2="959" y2="34" stroke="#00f2c3" stroke-width="0.8" stroke-opacity="0.25"/>

  <!-- Window Dots -->
  <circle cx="24" cy="17" r="4.5" fill="#ff5f56"/>
  <circle cx="40" cy="17" r="4.5" fill="#ffbd2e"/>
  <circle cx="56" cy="17" r="4.5" fill="#27c93f"/>

  <!-- Command Line in Center: Matching Reference Image -->
  <text x="480" y="21" text-anchor="middle" class="term-cmd">
    ~ $ <tspan fill="#00f2c3">./identity.sh --user dexterbeast0-cmyk</tspan>
  </text>

  <!-- Online Badge in Top Right -->
  <circle cx="878" cy="17" r="3.5" fill="#00f2c3" filter="url(#scan-flare)"/>
  <text x="888" y="21" class="online-badge">ONLINE</text>

  <!-- Cyber HUD Corner Brackets Matching Reference Image -->
  <g stroke="#00f2c3" stroke-width="1.6" stroke-linecap="square" fill="none" opacity="0.75">
    <!-- Top-Left -->
    <path d="M 28 58 L 28 46 L 40 46"/>
    <!-- Top-Right -->
    <path d="M 932 58 L 932 46 L 920 46"/>
    <!-- Bottom-Left -->
    <path d="M 28 148 L 28 160 L 40 160"/>
    <!-- Bottom-Right -->
    <path d="M 932 148 L 932 160 L 920 160"/>
  </g>

  <!-- ============================================================ -->
  <!-- LAYER 1: ULTRA-SUBTLE FAINT TERMINAL GHOST (DIM START)        -->
  <!-- ============================================================ -->
  <g class="ascii-base dim-ghost">
{dim_block}  </g>

  <!-- ============================================================ -->
  <!-- LAYER 2: PROGRESSIVE LETTER-BY-LETTER REVEAL IN CRISP GREY    -->
  <!-- Mask opens LEFT -> RIGHT revealing A -> AB -> ABH -> ...     -->
  <!-- ============================================================ -->
  <g mask="url(#ascii-reveal-mask)">
    <g class="ascii-base bright-grey" filter="url(#text-soft-glow)">
      <!-- Smooth dimming/fade at end of cycle back to dim/hidden -->
      <animate attributeName="opacity"
               values="1.0; 1.0; 1.0; 0.0; 1.0"
               keyTimes="0; 0.60; 0.70; 0.86; 1"
               dur="{dur}s"
               repeatCount="indefinite"
               calcMode="linear"/>
{bright_block}    </g>
  </g>

  <!-- ============================================================ -->
  <!-- LAYER 3: GLOSSY CYAN/GREEN SPECULAR REFLECTION SWEEP         -->
  <!-- Sweeps across revealed name after full reveal holds          -->
  <!-- ============================================================ -->
  <g mask="url(#ascii-reveal-mask)" pointer-events="none" filter="url(#scan-flare)">
    <rect x="-280" y="44" width="280" height="122" fill="url(#specular-streak)" opacity="0.85">
      <animate attributeName="x"
               values="-280; -280; 960; 960; -280"
               keyTimes="0; 0.70; 0.86; 0.94; 1"
               dur="{dur}s"
               repeatCount="indefinite"
               calcMode="spline"
               keySplines="0 0 1 1; 0.42 0 0.58 1; 0 0 1 1; 0 0 1 1"/>
    </rect>
  </g>

  <!-- ============================================================ -->
  <!-- LAYER 4: LUMINOUS SCANNING LINE (Sweeps with progressive mask)-->
  <!-- ============================================================ -->
  <g pointer-events="none" filter="url(#scan-flare)">
    <!-- Soft Glow Beam -->
    <rect x="46" y="46" width="24" height="116" rx="3" fill="url(#scanline-glow)">
      <animate attributeName="x"
               values="46; 918; 918; 46"
               keyTimes="0; 0.60; 0.86; 1"
               dur="{dur}s"
               repeatCount="indefinite"
               calcMode="linear"/>
      <animate attributeName="opacity"
               values="0.0; 1.0; 1.0; 0.0; 0.0; 0.0"
               keyTimes="0; 0.03; 0.58; 0.62; 0.86; 1"
               dur="{dur}s"
               repeatCount="indefinite"/>
    </rect>
    <!-- Sharp Core Laser -->
    <line x1="58" y1="46" x2="58" y2="162" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round">
      <animate attributeName="x1"
               values="58; 930; 930; 58"
               keyTimes="0; 0.60; 0.86; 1"
               dur="{dur}s"
               repeatCount="indefinite"
               calcMode="linear"/>
      <animate attributeName="x2"
               values="58; 930; 930; 58"
               keyTimes="0; 0.60; 0.86; 1"
               dur="{dur}s"
               repeatCount="indefinite"
               calcMode="linear"/>
      <animate attributeName="opacity"
               values="0.0; 1.0; 1.0; 0.0; 0.0; 0.0"
               keyTimes="0; 0.03; 0.58; 0.62; 0.86; 1"
               dur="{dur}s"
               repeatCount="indefinite"/>
    </line>
  </g>
</svg>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Successfully generated {output_path} ({len(svg_content)} bytes)")

if __name__ == "__main__":
    build_name_svg("name.svg")
