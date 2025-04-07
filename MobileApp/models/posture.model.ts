export interface PostureUpdate {
    posture: {
        posture: string;
        confidence: number;
        posture_vi: string;
        angles: {
           [key: string]: number;
        }
        need_alert: string;
    },
    timestamp: string;
}

export interface Statistics{
    total_time: number;
    posture_counts: {
        [key: string]: number;
    };
    posture_percentages: {
        [key: string]: number;
    };
    transitions: number;
}

export interface Frame extends PostureUpdate{
    image: string;
}