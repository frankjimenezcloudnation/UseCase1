import { api } from "@/api/client";

export type DocumentSource = "builtin" | "upload";

export interface DocumentInfo {
  id: string;
  filename: string;
  role: "fund" | "benchmark";
  doc_type: string;
  source: DocumentSource;
}

export interface DocumentsResponse {
  ai_configured: boolean;
  model: string;
  fund: DocumentInfo[];
  benchmark: DocumentInfo[];
}

export type MatchQuality = "exact" | "fuzzy" | "none";

export interface ProvisionSource {
  document_name: string;
  section: string;
  page_number: number;
  quote: string;
  verified: boolean;
  match_quality: MatchQuality;
}

export type Severity = "High" | "Medium" | "Low" | "None";
export type EvidenceLevel = "Hoog" | "Middel" | "Laag";

export interface EntitlementComparison {
  area: string;
  current_points: string[];
  standard_points: string[];
  key_differences: string[];
  current_detail: string;
  standard_detail: string;
  gap_detected: boolean;
  deviation_severity: Severity;
  impact_explanation: string;
  required_qwik_configuration: string;
  current_sources: ProvisionSource[];
  standard_sources: ProvisionSource[];
  evidence_verified: boolean;
  evidence_score: number;
  evidence_level: EvidenceLevel;
}

export interface FundComparisonReport {
  fund_name: string;
  target_transition_date: string;
  entitlements: EntitlementComparison[];
}

export interface AnalysisResponse {
  mode: "live" | "demo";
  model: string | null;
  fund_documents: string[];
  benchmark_documents: string[];
  cached: boolean;
  report: FundComparisonReport;
}

export interface AnalysisRequest {
  fund_document_ids: string[];
  benchmark_document_ids: string[];
}

export const analysisApi = {
  documents: () => api.get<DocumentsResponse>("/analysis/documents"),
  compare: (req: AnalysisRequest) => api.post<AnalysisResponse>("/analysis/compare", req),
  upload: (file: File, role?: "fund" | "benchmark") => {
    const form = new FormData();
    form.append("file", file);
    if (role) form.append("role", role);
    return api.postForm<DocumentsResponse>("/analysis/documents", form);
  },
  patch: (id: string, patch: { role?: "fund" | "benchmark"; doc_type?: string }) =>
    api.patch<DocumentsResponse>(`/analysis/documents/${id}`, patch),
  remove: (id: string) => api.del<DocumentsResponse>(`/analysis/documents/${id}`),
};

/** The FIXED set of themes analysed every run (kept in sync with backend CANONICAL_THEMES).
 *  Because the set is fixed, the same documents always yield the same themes. */
export const WTP_THEMES: string[] = [
  "Opbouwsystematiek",
  "Partnerpensioen",
  "Wezenpensioen",
  "Arbeidsongeschiktheid (premievrijstelling)",
  "Indexatie/Toeslagen",
  "Compensatie afschaffing doorsneesystematiek",
  "Beleggingsbeleid/Lifecycle",
  "Uitkeringsfase / Collectief Variabel Pensioen",
  "Risicodelingsreserve",
  "Invaren",
  "Bijsparen",
];
