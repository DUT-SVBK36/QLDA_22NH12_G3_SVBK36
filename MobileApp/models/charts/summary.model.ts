export interface Summary {
  total_sessions: number;
  first_session_date: string;
  latest_session_date: string;
  total_usage_time: number;
  good_posture_duration: number;
  bad_posture_duration: number;
  good_posture_percentage: number;
  bad_posture_percentage: number;
  corrected_postures: number;
}
