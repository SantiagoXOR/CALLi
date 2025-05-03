import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Call, CallDetail } from "@/types/call";
import { supabase } from "@/lib/supabase";

// Base URL for API calls
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Get calls with pagination and filters
export const getCalls = async (
  page: number = 1,
  pageSize: number = 10,
  filters: any = {}
) => {
  // Build query parameters
  const params = new URLSearchParams({
    page: page.toString(),
    page_size: pageSize.toString(),
    sort_by: "created_at",
    sort_order: "desc",
  });

  // Add filters to query parameters
  Object.entries(filters).forEach(([key, value]) => {
    if (value) {
      params.append(key, value as string);
    }
  });

  const response = await fetch(`${API_URL}/api/calls?${params.toString()}`, {
    headers: {
      Authorization: `Bearer ${(await supabase.auth.getSession()).data.session?.access_token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch calls");
  }

  return response.json();
};

// Get call detail
export const getCallDetail = async (callId: string) => {
  const response = await fetch(
    `${API_URL}/api/calls/${callId}?include_recordings=true&include_transcripts=true`,
    {
      headers: {
        Authorization: `Bearer ${(await supabase.auth.getSession()).data.session?.access_token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch call detail");
  }

  return response.json();
};

// Cancel call
export const cancelCall = async (callId: string) => {
  const response = await fetch(`${API_URL}/api/calls/${callId}/cancel`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${(await supabase.auth.getSession()).data.session?.access_token}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error("Failed to cancel call");
  }

  return response.json();
};

// Reschedule call
export const rescheduleCall = async (callId: string, scheduledTime: Date) => {
  const response = await fetch(`${API_URL}/api/calls/${callId}/reschedule`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${(await supabase.auth.getSession()).data.session?.access_token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ scheduled_time: scheduledTime.toISOString() }),
  });

  if (!response.ok) {
    throw new Error("Failed to reschedule call");
  }

  return response.json();
};

// React Query hooks
export const useGetCalls = (
  page: number = 1,
  pageSize: number = 10,
  filters: any = {}
) => {
  return useQuery({
    queryKey: ["calls", page, pageSize, filters],
    queryFn: () => getCalls(page, pageSize, filters),
  });
};

export const useGetCallDetail = (callId: string) => {
  return useQuery({
    queryKey: ["call", callId],
    queryFn: () => getCallDetail(callId),
    enabled: !!callId,
  });
};

export const useCancelCall = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (callId: string) => cancelCall(callId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["calls"] });
    },
  });
};

export const useRescheduleCall = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ callId, scheduledTime }: { callId: string; scheduledTime: Date }) =>
      rescheduleCall(callId, scheduledTime),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["calls"] });
    },
  });
};
