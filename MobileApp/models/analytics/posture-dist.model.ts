export interface PostureDistItem {
  count: number | null;
  name: string | null;
  duration: number | null;
  severity_level: number | null;
  percentage: number | null;
  duration_percentage: number | null;
}

export interface PostureDist {
  distribution: {
    [key: string]: PostureDistItem | null;
  } | null;
  total_items: number | null;
  total_duration: number | null;
}
