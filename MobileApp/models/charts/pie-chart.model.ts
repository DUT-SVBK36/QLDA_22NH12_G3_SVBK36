export interface PieChartDataPoint {
  value: number;
  color?: string;
  gradientCenterColor?: string;
  focused?: boolean;
  text?: string;
  textColor?: string;
  textBackgroundColor?: string;
  textSize?: number;
  shiftX?: number;
  shiftY?: number;
  labelPosition?: string;
  onPress?: () => void;
}
