import { Campaign, CampaignCreate, CampaignUpdate } from "@/types/campaign";
import {
  useMutation,
  UseMutationResult,
  useQuery,
  useQueryClient,
  UseQueryResult,
} from "@tanstack/react-query";
import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Endpoints
const ENDPOINTS = {
  CAMPAIGNS: "/api/campaigns",
  CAMPAIGN_BY_ID: (id: string) => `/api/campaigns/${id}`,
  CAMPAIGN_CLIENTS: (campaignId: string, clientId: string) =>
    `/api/campaigns/${campaignId}/clients/${clientId}`,
};

export const campaignService = {
  async getCampaigns(
    page = 1,
    limit = 10
  ): Promise<{ data: Campaign[]; total: number }> {
    const skip = (page - 1) * limit;
    const response = await axios.get(`${API_URL}/api/campaigns`, {
      params: { skip, limit },
    });
    return response.data;
  },

  async getCampaign(id: string): Promise<Campaign> {
    const response = await axios.get(`${API_URL}/api/campaigns/${id}`);
    return response.data;
  },

  async createCampaign(campaign: CampaignCreate): Promise<Campaign> {
    const response = await axios.post(`${API_URL}/api/campaigns`, campaign);
    return response.data;
  },

  async updateCampaign(
    id: string,
    campaign: CampaignUpdate
  ): Promise<Campaign> {
    const response = await axios.put(
      `${API_URL}/api/campaigns/${id}`,
      campaign
    );
    return response.data;
  },

  async deleteCampaign(id: string): Promise<{ success: boolean }> {
    const response = await axios.delete(`${API_URL}/api/campaigns/${id}`);
    return response.data;
  },

  async addClientToCampaign(
    campaignId: string,
    clientId: string
  ): Promise<{ success: boolean }> {
    const response = await axios.post(
      `${API_URL}/api/campaigns/${campaignId}/clients/${clientId}`
    );
    return response.data;
  },
};

// React Query hooks

export const useGetCampaigns = (
  page = 1,
  limit = 10
): UseQueryResult<{ data: Campaign[]; total: number }> => {
  return useQuery({
    queryKey: ["campaigns", page, limit],
    queryFn: () => campaignService.getCampaigns(page, limit),
  });
};

export const useGetCampaign = (id: string): UseQueryResult<Campaign> => {
  return useQuery({
    queryKey: ["campaign", id],
    queryFn: () => campaignService.getCampaign(id),
  });
};

export const useCreateCampaign = (): UseMutationResult<
  Campaign,
  Error,
  CampaignCreate
> => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (campaign: CampaignCreate) =>
      campaignService.createCampaign(campaign),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["campaigns"] });
    },
  });
};

export const useUpdateCampaign = (): UseMutationResult<
  Campaign,
  Error,
  { id: string; campaign: CampaignUpdate }
> => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, campaign }: { id: string; campaign: CampaignUpdate }) =>
      campaignService.updateCampaign(id, campaign),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["campaigns"] });
    },
  });
};

export const useDeleteCampaign = (): UseMutationResult<
  { success: boolean },
  Error,
  string
> => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => campaignService.deleteCampaign(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["campaigns"] });
    },
  });
};
