export interface PostureDurationItem {
  total_duration: number | null;
  count: number | null;
  avg_duration: number | null;
  max_duration: number | null;
  min_duration: number | null;
  name: string | null;
  severity_level: number | null;
  percentage: number | null;
}
export interface PostureDuration {
  durations: {
    good_sitting_side: PostureDurationItem | null;
    too_lean_right_side: PostureDurationItem | null;
    too_lean_left_side: PostureDurationItem | null;
    bad_sitting_backward_side: PostureDurationItem | null;
    bad_sitting_forward_side: PostureDurationItem | null;
    neck_wrong_position: PostureDurationItem | null;
    leg_wrong_position: PostureDurationItem | null;
  } | null;
  total_duration: number | null;
}
