import { AuthService } from "@/services/auth";

/**
 * Helper function to make authenticated API requests
 * @param url API endpoint URL
 * @param params Optional query parameters
 * @returns Parsed JSON response
 */
export async function fetchWithAuth<T>(
  url: string,
  params: Record<string, string> = {},
  options: RequestInit = {}
): Promise<T> {
  const token = await AuthService.getToken();
  if (!token) throw new Error("No authentication token found");

  // Build URL with query parameters
  const queryParams = new URLSearchParams(params).toString();
  const requestUrl = queryParams ? `${url}?${queryParams}` : url;

  const response = await fetch(requestUrl, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
    // Note: we're merging options but explicitly setting headers to ensure Authorization is included
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API request failed: ${response.status} ${errorText}`);
  }

  return await response.json();
}
