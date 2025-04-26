export enum CallStatus {
  QUEUED = "queued",
  RINGING = "ringing",
  IN_PROGRESS = "in_progress",
  COMPLETED = "completed",
  FAILED = "failed",
  CANCELLED = "cancelled",
  UNKNOWN = "unknown",
}

export interface Call {
  id: string;
  campaign_id: string;
  contact_id: string;
  phone_number: string;
  status: CallStatus;
  duration: number | null;
  recording_url: string | null;
  twilio_sid: string | null;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}

export interface CallDetail extends Call {
  campaign_name: string;
  contact_name: string;
  transcript: any[] | null;
  recordings: string[] | null;
}

export interface CallMetrics {
  total_calls: number;
  completed_calls: number;
  failed_calls: number;
  success_rate: number;
  avg_duration: number;
  by_status: Record<CallStatus, number>;
  timeline: {
    date: string;
    total: number;
    completed: number;
    failed: number;
  }[];
}
