---
name: CampusPulse
colors:
  surface: '#fcf8ff'
  surface-dim: '#dbd8e4'
  surface-bright: '#fcf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f2fe'
  surface-container: '#efecf8'
  surface-container-high: '#e9e6f3'
  surface-container-highest: '#e4e1ed'
  on-surface: '#1b1b23'
  on-surface-variant: '#464554'
  inverse-surface: '#303038'
  inverse-on-surface: '#f2effb'
  outline: '#767586'
  outline-variant: '#c7c4d7'
  surface-tint: '#494bd6'
  primary: '#4648d4'
  on-primary: '#ffffff'
  primary-container: '#6063ee'
  on-primary-container: '#fffbff'
  inverse-primary: '#c0c1ff'
  secondary: '#a43073'
  on-secondary: '#ffffff'
  secondary-container: '#fc79bd'
  on-secondary-container: '#76014e'
  tertiary: '#904900'
  on-tertiary: '#ffffff'
  tertiary-container: '#b55d00'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e1e0ff'
  primary-fixed-dim: '#c0c1ff'
  on-primary-fixed: '#07006c'
  on-primary-fixed-variant: '#2f2ebe'
  secondary-fixed: '#ffd8e7'
  secondary-fixed-dim: '#ffafd3'
  on-secondary-fixed: '#3d0026'
  on-secondary-fixed-variant: '#85145a'
  tertiary-fixed: '#ffdcc5'
  tertiary-fixed-dim: '#ffb783'
  on-tertiary-fixed: '#301400'
  on-tertiary-fixed-variant: '#703700'
  background: '#fcf8ff'
  on-background: '#1b1b23'
  surface-variant: '#e4e1ed'
typography:
  display:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  h1:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.3'
    letterSpacing: -0.01em
  h2:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.2'
    letterSpacing: 0.01em
  caption:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 32px
  xl: 48px
  container-margin: 24px
  gutter: 16px
---

## Brand & Style

The design system for CampusPulse is engineered to evoke feelings of clarity, transparency, and modern efficiency. It targets a student demographic that values speed and a sophisticated digital experience. By merging the precision of high-end fintech platforms with the ethereal lightness of Glassmorphism, the UI achieves a "digital-first" air that is both professional and approachable.

The style is characterized by deep breathing room (whitespace), hyper-rounded surfaces, and translucent depth. It avoids the heaviness of traditional banking apps, opting instead for a weightless, cloud-like aesthetic where information surfaces are layered and vibrant pastel accents guide the eye toward key actions.

## Colors

The palette centers on a soft off-white background that acts as a canvas for high-contrast white surfaces. Pure black is strictly prohibited; instead, a range of Slate and Gray tones provide depth and readability while maintaining a premium feel.

- **Background:** A cool, desaturated off-white (#F4F7FB) provides the base.
- **Surfaces:** Pure white (#FFFFFF) is used for cards and interactive elements to create distinction.
- **Accents:** Soft pastel gradients are used sparingly for progress bars, primary buttons, and status indicators. These gradients utilize a high-vibrance, low-saturation approach to maintain a professional fintech polish.
- **Status:** Mint green for "Success/Growth," Peach/Orange for "Warning," and a soft Red for "Alerts."

## Typography

This design system utilizes **Inter** for its exceptional readability and utilitarian charm. The typographic hierarchy is built on a high-contrast scale, ensuring that financial data and key metrics are immediately legible.

- **Headlines:** Use semi-bold or bold weights with slight negative letter-spacing to create a compact, modern look.
- **Body:** Standardized at 16px for optimal legibility. Use "Slate 600" for standard body text and "Slate 900" for emphasized content.
- **Labels:** Uppercase is rarely used; instead, medium-weight sentence-case labels provide a more friendly, less institutional tone.

## Layout & Spacing

The system follows a strict 8px grid, but favors generous padding to maintain the "ultra-clean" aesthetic. 

- **Grid Model:** A 12-column fluid grid for desktop and a single-column fluid grid for mobile. 
- **Inner Padding:** Cards and containers should never have less than 24px of internal padding to ensure the "Glass" effect doesn't feel cramped.
- **Rhythm:** Vertical rhythm is driven by the `md` (24px) unit, creating a sense of balance and openness between sections.

## Elevation & Depth

This design system eschews traditional heavy shadows in favor of **Glassmorphism** and ambient light effects. 

1. **Level 0 (Base):** The off-white background.
2. **Level 1 (Cards):** Pure white surfaces with a 1px border (#FFFFFF) and a very soft, multi-layered shadow: `0 10px 25px -5px rgba(0, 0, 0, 0.02), 0 8px 10px -6px rgba(0, 0, 0, 0.02)`.
3. **Level 2 (Modals/Overlays):** These utilize a backdrop-blur (minimum 12px) and 70% opacity white fill, creating a "frosted glass" effect that allows background colors to bleed through subtly.
4. **Interactive State:** Hovering over a card should slightly increase the shadow spread and move the element 2px upward on the Y-axis.

## Shapes

The geometry of the design system is unapologetically rounded. Large radii are essential to the fintech aesthetic, making the interface feel safe and modern.

- **Main Cards:** 24px to 32px corner radius.
- **Buttons:** 12px to 16px corner radius (or fully pill-shaped for secondary actions).
- **Form Inputs:** 12px corner radius.
- **Consistency:** If an element is nested inside another, its radius should be `Parent Radius - Inner Padding` to maintain visual harmony.

## Components

- **Buttons:** Primary buttons use the "Ocean" gradient with white text and a soft glow shadow that matches the gradient color at 20% opacity. Secondary buttons are ghost-styled with a subtle 1px border.
- **Cards:** The core of the UI. Must have a pure white background, 32px rounded corners, and include a subtle inner 1px white stroke to define the edges against the off-white background.
- **Inputs:** Ultra-minimalist. Backgrounds are a slightly darker gray (#EDF2F7) than the main background, turning white on focus with a primary-colored glow.
- **Glass Chips:** Small status indicators with a high backdrop-blur and 20% opacity of their respective status color (e.g., 20% Mint Green for "Paid").
- **Icons:** Use **Lucide-react** line icons. Stroke weight should be set to 1.5px or 2px. Icons should be monochrome (Slate 500) unless they are being used within an accent-colored button or active navigation item.
- **Progress Bars:** Thicker bars (8px+) with fully rounded ends, using the pastel gradients to indicate completion or budget allocation.