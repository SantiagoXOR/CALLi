import { useQuery } from "@tanstack/react-query";
import { CallMetrics } from "@/types/call";
import { supabase } from "@/lib/supabase";

// Base URL for API calls
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Get call metrics
export const getCallMetrics = async (filters: any = {}) => {
  // Build query parameters
  const params = new URLSearchParams();
  
  if (filters.campaign_id) {
    params.append("campaign_id", filters.campaign_id);
  }
  
  if (filters.start_date) {
    params.append("start_date", filters.start_date.toISOString());
  }
  
  if (filters.end_date) {
    params.append("end_date", filters.end_date.toISOString());
  }
  
  if (filters.group_by) {
    params.append("group_by", filters.group_by);
  }
  
  const response = await fetch(`${API_URL}/api/reports/performance_metrics?${params.toString()}`, {
    headers: {
      Authorization: `Bearer ${(await supabase.auth.getSession()).data.session?.access_token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch call metrics");
  }

  return response.json() as Promise<CallMetrics>;
};

// Get campaign performance
export const getCampaignPerformance = async (filters: any = {}) => {
  // Build query parameters
  const params = new URLSearchParams();
  
  if (filters.start_date) {
    params.append("start_date", filters.start_date.toISOString());
  }
  
  if (filters.end_date) {
    params.append("end_date", filters.end_date.toISOString());
  }
  
  const response = await fetch(`${API_URL}/api/reports/campaigns/performance?${params.toString()}`, {
    headers: {
      Authorization: `Bearer ${(await supabase.auth.getSession()).data.session?.access_token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch campaign performance");
  }

  return response.json();
};

// Get call history
export const getCallHistory = async (
  page: number = 1,
  pageSize: number = 10,
  filters: any = {}
) => {
  // Build query parameters
  const params = new URLSearchParams({
    page: page.toString(),
    page_size: pageSize.toString(),
  });
  
  if (filters.campaign_id) {
    params.append("campaign_id", filters.campaign_id);
  }
  
  if (filters.contact_id) {
    params.append("contact_id", filters.contact_id);
  }
  
  if (filters.start_date) {
    params.append("start_date", filters.start_date.toISOString());
  }
  
  if (filters.end_date) {
    params.append("end_date", filters.end_date.toISOString());
  }
  
  const response = await fetch(`${API_URL}/api/reports/call_history?${params.toString()}`, {
    headers: {
      Authorization: `Bearer ${(await supabase.auth.getSession()).data.session?.access_token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch call history");
  }

  return response.json();
};

// Get campaign summary
export const getCampaignSummary = async (campaignId: string) => {
  const response = await fetch(`${API_URL}/api/reports/campaign/${campaignId}/summary`, {
    headers: {
      Authorization: `Bearer ${(await supabase.auth.getSession()).data.session?.access_token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch campaign summary");
  }

  return response.json();
};

// React Query hooks
export const useGetCallMetrics = (filters: any = {}) => {
  return useQuery({
    queryKey: ["callMetrics", filters],
    queryFn: () => getCallMetrics(filters),
  });
};

export const useGetCampaignPerformance = (filters: any = {}) => {
  return useQuery({
    queryKey: ["campaignPerformance", filters],
    queryFn: () => getCampaignPerformance(filters),
  });
};

export const useGetCallHistory = (
  page: number = 1,
  pageSize: number = 10,
  filters: any = {}
) => {
  return useQuery({
    queryKey: ["callHistory", page, pageSize, filters],
    queryFn: () => getCallHistory(page, pageSize, filters),
  });
};

export const useGetCampaignSummary = (campaignId: string) => {
  return useQuery({
    queryKey: ["campaignSummary", campaignId],
    queryFn: () => getCampaignSummary(campaignId),
    enabled: !!campaignId,
  });
};
