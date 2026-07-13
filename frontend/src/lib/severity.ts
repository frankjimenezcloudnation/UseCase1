import type { Severity } from "@/api/analysis";

export interface SeverityMeta {
  label: string; // Dutch, plain-language
  color: string; // solid accent
  bg: string; // soft background
  fg: string; // text on the solid accent
  description: string;
}

export const SEVERITY: Record<Severity, SeverityMeta> = {
  High: {
    label: "Hoog",
    color: "#FE5E3E",
    bg: "#FEECE8",
    fg: "white",
    description: "Grote afwijking — vraagt actie en maatwerk bij de overgang.",
  },
  Medium: {
    label: "Middel",
    color: "#E8920C",
    bg: "#FDF1DD",
    fg: "black",
    description: "Aandachtspunt — bewuste keuze nodig bij de inrichting.",
  },
  Low: {
    label: "Laag",
    color: "#2EBDA9",
    bg: "#E4F6F3",
    fg: "black",
    description: "Kleine afwijking — beperkte impact op de deelnemer.",
  },
  None: {
    label: "Geen",
    color: "#9AA0A6",
    bg: "#EFEDEA",
    fg: "black",
    description: "Sluit aan op het standaardproduct.",
  },
};

export const SEVERITY_ORDER: Severity[] = ["High", "Medium", "Low", "None"];
