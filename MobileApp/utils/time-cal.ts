/**
 * Calculates the difference between a given date and now, returning a human-readable string
 * @param date The date to compare with now
 * @returns A string describing the time difference (e.g., "2 hours ago", "just now", "in 5 minutes")
 */
export function getTimeAgo(date: Date | string | number): string {
    const now = new Date();
    const inputDate = new Date(date);
    const diffInSeconds = Math.floor((now.getTime() - inputDate.getTime()) / 1000);
    const isPast = diffInSeconds >= 0;
    const absDiff = Math.abs(diffInSeconds);

    // Define time intervals in seconds
    const minute = 60;
    const hour = minute * 60;
    const day = hour * 24;
    const week = day * 7;
    const month = day * 30;
    const year = day * 365;

    // Just now (within 30 seconds)
    if (absDiff < 30) {
        return "just now";
    }

    let value: number;
    let unit: string;

    if (absDiff < minute) {
        value = absDiff;
        unit = "second";
    } else if (absDiff < hour) {
        value = Math.floor(absDiff / minute);
        unit = "minute";
    } else if (absDiff < day) {
        value = Math.floor(absDiff / hour);
        unit = "hour";
    } else if (absDiff < week) {
        value = Math.floor(absDiff / day);
        unit = "day";
    } else if (absDiff < month) {
        value = Math.floor(absDiff / week);
        unit = "week";
    } else if (absDiff < year) {
        value = Math.floor(absDiff / month);
        unit = "month";
    } else {
        value = Math.floor(absDiff / year);
        unit = "year";
    }

    // Add plural 's' if the value is not 1
    if (value !== 1) {
        unit += "s";
    }

    return isPast ? `${value} ${unit} ago` : `in ${value} ${unit}`;
}