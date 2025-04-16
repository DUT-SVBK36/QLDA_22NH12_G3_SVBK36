import { ChartDataPoint } from "./base.model";

export interface BarChartDataPoint extends ChartDataPoint {
  barWidth?: number;
  spacing?: number;
  capRadius?: number;
  capColor?: string;
  labelComponent?: React.ReactNode;
  topLabelComponent?: React.ReactNode;
  topLabelComponentHeight?: number;
  barBorderRadius?: number;
  disablePress?: boolean;
  showGradient?: boolean;
  gradientColor?: string;
  borderWidth?: number;
  borderColor?: string;
}

export interface StackedBarDataPoint extends Omit<BarChartDataPoint, "value"> {
  stacks: {
    value: number;
    color?: string;
    marginBottom?: number;
    borderRadius?: number;
    label?: string;
  }[];
}

export interface MultipleBarDataPoint {
  label?: string;
  bars: {
    value: number;
    color?: string;
    borderRadius?: number;
    disablePress?: boolean;
    showGradient?: boolean;
    gradientColor?: string;
    label?: string;
    barWidth?: number;
    spacing?: number;
    labelTextStyle?: any;
  }[];
}
