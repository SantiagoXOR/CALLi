import axios from 'axios';
import { Campaign, CampaignCreate, CampaignUpdate } from '../types/campaign';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const campaignApi = {
  // Obtener todas las campañas
  async getCampaigns(): Promise<Campaign[]> {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/campaigns`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener campañas:', error);
      throw error;
    }
  },

  // Obtener una campaña por ID
  async getCampaignById(id: string): Promise<Campaign> {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/campaigns/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error al obtener campaña con ID ${id}:`, error);
      throw error;
    }
  },

  // Crear una nueva campaña
  async createCampaign(campaign: CampaignCreate): Promise<Campaign> {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/campaigns`, campaign);
      return response.data;
    } catch (error) {
      console.error('Error al crear campaña:', error);
      throw error;
    }
  },

  // Actualizar una campaña existente
  async updateCampaign(id: string, campaign: CampaignUpdate): Promise<Campaign> {
    try {
      const response = await axios.put(`${API_BASE_URL}/api/campaigns/${id}`, campaign);
      return response.data;
    } catch (error) {
      console.error(`Error al actualizar campaña con ID ${id}:`, error);
      throw error;
    }
  },

  // Eliminar una campaña
  async deleteCampaign(id: string): Promise<void> {
    try {
      await axios.delete(`${API_BASE_URL}/api/campaigns/${id}`);
    } catch (error) {
      console.error(`Error al eliminar campaña con ID ${id}:`, error);
      throw error;
    }
  },

  // Obtener estadísticas de una campaña
  async getCampaignStats(id: string): Promise<any> {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/campaigns/${id}/stats`);
      return response.data;
    } catch (error) {
      console.error(`Error al obtener estadísticas de campaña con ID ${id}:`, error);
      throw error;
    }
  }
};
