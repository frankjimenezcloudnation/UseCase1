import { ChakraProvider, defaultSystem } from "@chakra-ui/react";
import { ThemeProvider } from "next-themes";
import type { PropsWithChildren } from "react";

/**
 * Wraps the app in Chakra UI's provider plus color-mode (light/dark) support
 * via next-themes. Extend `defaultSystem` with `createSystem` to customize the
 * theme (tokens, colors, fonts).
 */
export function Provider({ children }: PropsWithChildren) {
  return (
    <ChakraProvider value={defaultSystem}>
      <ThemeProvider attribute="class" disableTransitionOnChange>
        {children}
      </ThemeProvider>
    </ChakraProvider>
  );
}
