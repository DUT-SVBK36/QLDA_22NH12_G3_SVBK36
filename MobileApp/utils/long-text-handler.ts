/**
 * Utility to handle long text by truncating it and adding ellipsis
 * @param text The text to truncate
 * @param maxLength The maximum length allowed before truncation
 * @param ellipsis The string to append after truncation (default: '...')
 * @returns Truncated text with ellipsis if needed, or the original text if not exceeding maxLength
 */
export const truncateText = (
    text: string,
    maxLength: number,
    ellipsis: string = '...'
): string => {
    if (!text) return '';
    
    if (text.length <= maxLength) {
        return text;
    }
    
    // Account for the ellipsis length in the truncation
    const truncatedLength = maxLength - ellipsis.length;
    return text.slice(0, truncatedLength > 0 ? truncatedLength : 0) + ellipsis;
};

/**
 * Check if text needs to be truncated
 * @param text The text to check
 * @param maxLength The maximum length threshold
 * @returns Boolean indicating if text exceeds maxLength
 */
export const needsTruncation = (text: string, maxLength: number): boolean => {
    if (!text) return false;
    return text.length > maxLength;
};