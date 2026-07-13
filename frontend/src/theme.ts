import { createSystem, defaultConfig, defineConfig } from "@chakra-ui/react";

// CloudNation brand tokens — Brand Guidelines v1.1 ("Enable. Empower. Deliver.")
const config = defineConfig({
  globalCss: {
    "html, body": {
      bg: "bg.canvas",
      color: "fg.default",
      fontFamily: "body",
    },
  },
  theme: {
    tokens: {
      fonts: {
        heading: {
          value: "'Epilogue', 'Helvetica Neue', Arial, sans-serif",
        },
        body: {
          value: "'Mulish', 'Avenir', 'Nunito Sans', system-ui, sans-serif",
        },
        mono: { value: "ui-monospace, 'JetBrains Mono', Menlo, monospace" },
      },
      colors: {
        marvel: {
          50: { value: "#EAF7FF" },
          100: { value: "#C9ECFF" },
          200: { value: "#9FDCFF" },
          300: { value: "#5FC6FF" },
          400: { value: "#1FB6FF" }, // brand primary — Marvelblauw
          500: { value: "#0E9FE6" },
          600: { value: "#0E83BF" },
          700: { value: "#0E6796" },
          800: { value: "#0B4E71" },
          900: { value: "#08374F" },
        },
        pastinaak: { value: "#F8F5F2" },
        guaverood: { value: "#FE5E3E" },
        mintgroen: { value: "#2EBDA9" },
      },
    },
    semanticTokens: {
      colors: {
        "bg.canvas": { value: "{colors.pastinaak}" },
        "fg.default": { value: "#111111" },
        "fg.muted": { value: "#5B5B60" },
        brand: {
          solid: { value: "{colors.marvel.400}" },
          contrast: { value: "#000000" },
          fg: { value: "{colors.marvel.700}" },
          muted: { value: "{colors.marvel.100}" },
          subtle: { value: "{colors.marvel.50}" },
          emphasized: { value: "{colors.marvel.500}" },
          focusRing: { value: "{colors.marvel.400}" },
        },
      },
    },
  },
});

export const system = createSystem(defaultConfig, config);
