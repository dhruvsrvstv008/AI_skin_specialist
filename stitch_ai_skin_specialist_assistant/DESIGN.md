---
name: Clinical Clarity
colors:
  surface: '#f9f9ff'
  surface-dim: '#d3daef'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f3ff'
  surface-container: '#e9edff'
  surface-container-high: '#e1e8fd'
  surface-container-highest: '#dce2f7'
  on-surface: '#141b2b'
  on-surface-variant: '#434655'
  inverse-surface: '#293040'
  inverse-on-surface: '#edf0ff'
  outline: '#747686'
  outline-variant: '#c4c5d7'
  surface-tint: '#2151da'
  primary: '#0037b0'
  on-primary: '#ffffff'
  primary-container: '#1d4ed8'
  on-primary-container: '#cad3ff'
  inverse-primary: '#b7c4ff'
  secondary: '#505f76'
  on-secondary: '#ffffff'
  secondary-container: '#d0e1fb'
  on-secondary-container: '#54647a'
  tertiary: '#00496b'
  on-tertiary: '#ffffff'
  tertiary-container: '#00628d'
  on-tertiary-container: '#abdaff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dce1ff'
  primary-fixed-dim: '#b7c4ff'
  on-primary-fixed: '#001551'
  on-primary-fixed-variant: '#0039b5'
  secondary-fixed: '#d3e4fe'
  secondary-fixed-dim: '#b7c8e1'
  on-secondary-fixed: '#0b1c30'
  on-secondary-fixed-variant: '#38485d'
  tertiary-fixed: '#c9e6ff'
  tertiary-fixed-dim: '#89ceff'
  on-tertiary-fixed: '#001e2f'
  on-tertiary-fixed-variant: '#004c6e'
  background: '#f9f9ff'
  on-background: '#141b2b'
  surface-variant: '#dce2f7'
  surface-subtle: '#F9FAFB'
  border-light: '#E5E7EB'
  status-success: '#10B981'
  status-error: '#EF4444'
typography:
  display-lg:
    fontFamily: IBM Plex Sans
    fontSize: 48px
    fontWeight: '600'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: IBM Plex Sans
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: IBM Plex Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: IBM Plex Sans
    fontSize: 24px
    fontWeight: '500'
    lineHeight: 32px
  body-lg:
    fontFamily: IBM Plex Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: IBM Plex Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: IBM Plex Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: IBM Plex Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: IBM Plex Sans
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 14px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-margin: 24px
  gutter: 16px
  section-gap: 64px
  component-padding-x: 16px
  component-padding-y: 12px
---

## Brand & Style
The design system is engineered for the high-stakes environment of premium healthcare SaaS. It balances clinical precision with an approachable, patient-centric warmth. The brand personality is authoritative yet empathetic, focusing on clarity, speed of information retrieval, and absolute reliability.

The visual style is **Corporate / Modern** with a lean toward **Minimalism**. It utilizes expansive white space to reduce cognitive load and heavy emphasis on typographic hierarchy to ensure critical medical data is never obscured. The aesthetic avoids decorative flourishes in favor of functional elegance, creating a "breathable" interface that feels calm under pressure.

## Colors
The palette is rooted in medical tradition but modernized for high-density software. 
- **Primary Action:** A dependable medium-deep blue (#1D4ED8) used for primary CTA buttons, active states, and essential navigational cues.
- **Surface & Background:** The primary background is pure white (#FFFFFF), with secondary surfaces using a cool-gray (#F9FAFB) to differentiate content sections without creating harsh visual breaks.
- **Typography:** All primary text uses a deep navy-charcoal (#111827) to maximize contrast and readability against white backgrounds.
- **Borders:** Thin, subtle gray strokes (#E5E7EB) are used to define containers instead of shadows, maintaining a flat, clean, and clinical appearance.

## Typography
This design system exclusively uses **IBM Plex Sans** to leverage its technical, industrial-yet-humanist character. It is a font designed for readability in complex interfaces.

- **Headlines:** Use a medium-bold weight to establish clear hierarchy. Display styles should use slight negative letter-spacing for a more premium, compact feel.
- **Body Copy:** Set with generous line height (1.5x minimum) to prevent "wall of text" fatigue in medical reports.
- **Labels:** Small labels and data headers should use slightly increased letter-spacing and medium weights to remain legible at small scales.
- **Scalability:** Large headlines automatically downscale for mobile views to prevent excessive wrapping on smaller devices.

## Layout & Spacing
The layout follows a **Fluid Grid** model based on an 8px square rhythm. 

- **Desktop:** 12-column grid with 24px margins and 16px gutters. Content should be centered with a max-width of 1440px for dashboard views.
- **Tablet:** 8-column grid with 24px margins.
- **Mobile:** 4-column grid with 16px margins. 
- **Rhythm:** Use "Generous Whitespace" as a functional tool. Sections should be separated by large gaps (64px+) to clearly group related medical data. Information density should be kept low to medium to ensure critical alerts are not missed.

## Elevation & Depth
In alignment with the clinical aesthetic, this design system avoids heavy shadows. 

- **Flat Hierarchy:** Depth is primarily conveyed through **Tonal Layers**. Secondary content sits on `surface-subtle` (#F9FAFB), while primary content sits on white containers.
- **Low-Contrast Outlines:** Use 1px solid borders (#E5E7EB) for cards and inputs. 
- **Subtle Interaction Shadows:** Only use a very soft, diffused ambient shadow (0px 4px 12px, 5% opacity) when an element is hovered or "active" to provide tactile feedback without cluttering the visual plane.
- **Overlays:** Modals and dropdowns use a slightly more pronounced shadow to separate them from the base layer, accompanied by a 20% opacity navy backdrop blur.

## Shapes
The shape language uses **Rounded** (Level 2) geometry to soften the clinical precision and make the software feel more "friendly" and modern.

- **Standard Elements:** Buttons, input fields, and small cards use 0.5rem (8px) corner radii.
- **Large Containers:** Dashboard widgets and main content sections use `rounded-lg` (16px) or `rounded-xl` (24px) to create a premium, "app-like" feel.
- **Circular Elements:** Avatars and status indicators remain fully circular (pill-shaped) to distinguish them from functional UI components.

## Components
- **Buttons:** Primary buttons are solid Blue (#1D4ED8) with white text. Secondary buttons use a light gray stroke and navy text. Use large padding (12px 24px) to ensure a high tap target.
- **Inputs:** Fields are white with a 1px gray border. On focus, the border changes to the primary blue with a subtle 2px blue "halo" glow (low opacity).
- **Cards:** Cards should have no shadow by default, utilizing a 1px border and 16px rounded corners. Use a `surface-subtle` header area to group titles.
- **Chips/Badges:** Use semi-transparent versions of status colors (e.g., light green background with dark green text for "Healthy") to indicate status without the visual weight of a full button.
- **Data Lists:** Use alternating row colors or subtle 1px dividers. Ensure vertical cell padding is at least 16px to maintain the "premium SaaS" whitespace.
- **Navigation:** A clean left-hand sidebar using the deep navy text and icons, with a light blue "indicator bar" on the left edge for the active state.