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
    good_sitting_side: PostureDistItem | null;
    too_lean_right_side: PostureDistItem | null;
    too_lean_left_side: PostureDistItem | null;
    bad_sitting_backward_side: PostureDistItem | null;
    bad_sitting_forward_side: PostureDistItem | null;
    neck_wrong_position: PostureDistItem | null;
    leg_wrong_position: PostureDistItem | null;
  } | null;
  total_items: number | null;
  total_duration: number | null;
}
