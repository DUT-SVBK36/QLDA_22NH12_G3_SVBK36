export interface ImprovementItem {
  session_id: string | null;
  date: string | null;
  good_posture_count: number | null;
  bad_posture_count: number | null;
  total_count: number | null;
  good_percentage: number | null;
  bad_percentage: number | null;
}

export interface PostureImprovement {
  improvement_data: ImprovementItem[] | null;
}
