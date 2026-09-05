#!/usr/bin/env python3
"""
scripts/make_portrait.py

Master Entrypoint for GitSkins Cyber Terminal Profile Generation.
Regenerates:
- name.svg (Top terminal wordmark)
- ascii.svg (Hero terminal scan with VISUAL.MAP + SYSTEM.INFO)
- assets/cards/*.svg (Complete glossy glass card suite)

Engineered for Abhay Pratap Singh (dexterbeast0-cmyk/dexterbeast0-cmyk)
Visually calibrated to match reference test.mp4.
"""

import os
import sys

# Add scripts directory to path if needed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_cards

def main():
    print("=" * 60)
    print("REGENERATING CYBER TERMINAL PROFILE & CARDS (test.mp4 visual system)")
    print("=" * 60)
    generate_cards.main()
    print("=" * 60)
    print("All profile assets regenerated successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
