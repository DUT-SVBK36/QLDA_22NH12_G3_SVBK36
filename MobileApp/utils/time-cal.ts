/**
 * Calculates the difference between a given date and now, returning a human-readable string
 * @param date The date to compare with now
 * @returns A string describing the time difference (e.g., "2 hours ago", "just now", "in 5 minutes")
 */
export function getTimeAgo(date: Date | string | number): string {
  const now = new Date();
  const inputDate = new Date(date);
  const diffInSeconds = Math.floor(
    (now.getTime() - inputDate.getTime()) / 1000
  );
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
/**
 * Gets the start and end dates of the week containing the given date
 * @param date The date to find the week for (defaults to current date)
 * @param startOnMonday Whether the week starts on Monday (true) or Sunday (false, default)
 * @returns An object with start and end dates of the week
 */
export function getCurrentWeekByDate(
  date: Date | string | number = new Date(),
  startOnMonday: boolean = false
): { start: Date; end: Date } {
  const inputDate = new Date(date);
  const day = inputDate.getDay(); // 0 = Sunday, 1 = Monday, ..., 6 = Saturday

  // Calculate days to subtract to get to the start of the week
  const daysToStart = startOnMonday ? (day === 0 ? 6 : day - 1) : day;

  // Create start date
  const start = new Date(inputDate);
  start.setDate(inputDate.getDate() - daysToStart);
  start.setHours(0, 0, 0, 0);

  // Create end date (6 days after start)
  const end = new Date(start);
  end.setDate(start.getDate() + 6);
  end.setHours(23, 59, 59, 999);

  return { start, end };
}
