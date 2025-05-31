import config from "./config";

const api = {
  auth: {
    login: `${config.API_URL}/auth/token`,
    register: `${config.API_URL}/auth/register`,
    me: `${config.API_URL}/auth/me`,
  },
  session: {
    get: `${config.API_URL}/sessions/`,
    getById: (id: string) => `${config.API_URL}/sessions/${id}`,
    getLatest: `${config.API_URL}/sessions/latest`,
    getItem: (id: string) => `${config.BASE_URL}/sessions/items/${id}`,
  },
  analytics: {
    getPostureDist: `${config.API_URL}/analytics/distribution`,
    getPostureDuration: `${config.API_URL}/analytics/duration`,
    getPostureHistory: `${config.API_URL}/analytics/history`,
    getPostureImprovement: `${config.API_URL}/analytics/improvement`,
    getPostureDailySum: `${config.API_URL}/analytics/daily-summary`,
  },
};

export default api;
