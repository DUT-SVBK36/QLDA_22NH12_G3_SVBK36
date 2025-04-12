import api from "@/constants/api";
import { AuthService } from "./auth";
import { Session } from "@/models/session.model";

/**
 * Response format for multiple sessions
 */
export interface SessionsResponse {
  sessions: Session[];
}
export interface SessionItem {
  _id: string;
  timestamp: number;
  image: string;
  label_name: string;
  accuracy: number;
  label_recommendation?: string;
}

/**
 * Session service for handling session-related API calls
 */
export class SessionService {
  /**
   * Get all sessions with optional pagination
   * @param page Page number (starting from 1)
   * @param size Number of sessions per page
   * @returns Promise with sessions response
   */
  static async getAllSessions(
    page: number = 0,
    size: number = 10
  ): Promise<Session[]> {
    try {
      // Get auth token
      const token = await AuthService.getToken();
      console.log("token:", token);
      if (!token) {
        throw new Error("Authentication required");
      }

      // Build URL with query parameters
      const url = new URL(api.session.get);
      url.searchParams.append("skip", page.toString());
      url.searchParams.append("limit", size.toString());

      // Make API call
      const response = await fetch(url.toString(), {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || `Failed to fetch sessions: ${response.status}`
        );
      }
      const data = await response.json();
      console.log("Sessions data:", data); // Log the data for debugging

      return data;
    } catch (error) {
      console.error("Error fetching sessions:", error);
      throw error;
    }
  }

  /**
   * Get a specific session by ID
   * @param sessionId The ID of the session to retrieve
   * @returns Promise with session data
   */
  static async getSessionById(sessionId: string): Promise<Session> {
    try {
      // Get auth token
      const token = await AuthService.getToken();
      if (!token) {
        throw new Error("Authentication required");
      }

      // Make API call using the endpoint from api.ts
      const response = await fetch(api.session.getById(sessionId), {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || `Failed to fetch session: ${response.status}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error(`Error fetching session ${sessionId}:`, error);
      throw error;
    }
  }

  /**
   * Get the latest session for the current user
   * @returns Promise with the latest session data
   */
  static async getLatestSession(): Promise<Session | null> {
    try {
      // Get auth token
      const token = await AuthService.getToken();

      if (!token) {
        throw new Error("Authentication required");
      }

      // Make API call using the latest endpoint from api.ts
      const response = await fetch(api.session.getLatest, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.status === 404) {
        // No sessions found, return null instead of throwing error
        return null;
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail ||
            `Failed to fetch latest session: ${response.status}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error("Error fetching latest session:", error);
      throw error;
    }
  }
  static async getSessionItem(itemId: string): Promise<SessionItem> {
    try {
        const token = await AuthService.getToken();
        if (!token) {
            throw new Error("Authentication required");
        }

        // Debug log
        console.log('Making request to:', api.session.getItem(itemId));
        console.log('With token:', token);

        const response = await fetch(api.session.getItem(itemId), {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            credentials: 'include'
        });

        // Debug log
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error('Error response:', errorData); // Debug log
            throw new Error(
                errorData.detail || `Failed to fetch session item: ${response.status}`
            );
        }

        const data = await response.json();
        console.log('Success response:', data); // Debug log
        return data;
    } catch (error) {
        console.error(`Error fetching session item ${itemId}:`, error);
        throw error;
    }
}
  
}
