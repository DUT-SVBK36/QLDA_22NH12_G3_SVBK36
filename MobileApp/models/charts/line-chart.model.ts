import { ChartDataPoint } from "./base.model";

export interface LineChartDataPoint extends ChartDataPoint {
  date?: Date | string | number;
  dateLabel?: string;
  showDataPoint?: boolean;
  lineDashPattern?: number[];
  lineColor?: string;
}
