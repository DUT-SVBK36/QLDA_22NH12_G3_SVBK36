export interface HistoryItem {
  id: string;
  session_id: string;
  label_id: string;
  label_name: string;
  start_time: string;
  end_time: string;
  duration: number;
  accuracy: number;
}
export interface PostureHistory {
  history: HistoryItem[];
  total_items: number;
}
