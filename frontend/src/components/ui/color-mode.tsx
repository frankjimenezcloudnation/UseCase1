import { IconButton, type IconButtonProps } from "@chakra-ui/react";
import { useTheme } from "next-themes";
import { LuMoon, LuSun } from "react-icons/lu";

/** Toggles between light and dark color mode. */
export function ColorModeButton(props: Omit<IconButtonProps, "aria-label">) {
  const { theme, setTheme } = useTheme();
  const isDark = theme === "dark";
  return (
    <IconButton
      aria-label="Toggle color mode"
      variant="ghost"
      onClick={() => setTheme(isDark ? "light" : "dark")}
      {...props}
    >
      {isDark ? <LuSun /> : <LuMoon />}
    </IconButton>
  );
}
