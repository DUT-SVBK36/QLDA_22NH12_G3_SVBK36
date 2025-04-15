export interface SessionItem {
  _id: string;
  session_id: string;
  timestamp: number | string;
  accuracy: number;
  image?: string;
  image_path?: string;
  start_timestamp?: number;
  end_timestamp?: number;
  label_name: string;
  label_id: string;
  label_recommendation?: string;
}

export interface Session {
  _id: string;
  user_id: string;
  creation_date: string;
  items?: SessionItem[];
}
