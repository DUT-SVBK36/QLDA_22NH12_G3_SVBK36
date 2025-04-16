export interface PostureDailySum {
    date: string | null;
    total_sessions: number | null;
    total_duration: number | null;
    posture_distribution: any | null;
    posture_duration: any[] | null;
}