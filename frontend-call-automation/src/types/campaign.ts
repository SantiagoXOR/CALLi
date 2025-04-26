export interface Campaign {
  id: string;
  name: string;
  description: string;
  status: string;
  script_template: string;
  contact_list_ids: string[];
  schedule_start: string;
  schedule_end: string;
  calling_hours_start: string;
  calling_hours_end: string;
  max_retries: number;
  retry_delay_minutes: number;
  total_calls?: number;
  successful_calls?: number;
}

export interface CampaignCreate {
  name: string;
  description: string;
  status: string;
  script_template: string;
  contact_list_ids: string[];
  schedule_start: string;
  schedule_end: string;
  calling_hours_start: string;
  calling_hours_end: string;
  max_retries: number;
  retry_delay_minutes: number;
}

export interface CampaignUpdate {
  id: string;
  name: string;
  description: string;
  status: string;
  script_template: string;
  contact_list_ids: string[];
  schedule_start: string;
  schedule_end: string;
  calling_hours_start: string;
  calling_hours_end: string;
  max_retries: number;
  retry_delay_minutes: number;
}
