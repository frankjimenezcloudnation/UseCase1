import { api } from "@/api/client";

export interface DocumentInfo {
  id: string;
  filename: string;
  role: "fund" | "benchmark";
  doc_type: string;
}

export interface DocumentsResponse {
  ai_configured: boolean;
  model: string;
  fund: DocumentInfo[];
  benchmark: DocumentInfo[];
}

export interface ProvisionSource {
  document_name: string;
  section: string;
  page_number: number;
  quote: string;
}

export type Severity = "High" | "Medium" | "Low" | "None";

export interface EntitlementComparison {
  area: string;
  current_entitlement_description: string;
  standard_offering_description: string;
  gap_detected: boolean;
  deviation_severity: Severity;
  actuarial_implication: string;
  required_qwik_configuration: string;
  sources: ProvisionSource[];
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
  report: FundComparisonReport;
}

export interface AnalysisRequest {
  fund_document_ids: string[];
  benchmark_document_ids: string[];
}

export const analysisApi = {
  documents: () => api.get<DocumentsResponse>("/analysis/documents"),
  compare: (req: AnalysisRequest) => api.post<AnalysisResponse>("/analysis/compare", req),
};
