import config from "./config";

const api = {
  auth: {
    login: `${config.API_URL}/auth/token`,
    register: `${config.API_URL}/auth/register`,
  },
  session: {
    get: `${config.API_URL}/sessions/`,
    getById: (id: string) => `${config.API_URL}/sessions/${id}`,
    getLatest: `${config.API_URL}/sessions/latest`,
    getItem: (id: string) => `${config.BASE_URL}/sessions/items/${id}`,
  },
};

export default api;
