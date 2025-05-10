const ip = "192.168.111.113:8000";

const config = {
  BASE_URL: `http://${ip}/`,
  API_URL: `http://${ip}/api`,
  CAMERA_URL: `http://192.168.111.93:81/stream`,

  //Socket configuration
  SOCKET_URL: `ws://${ip}/api/ws`,
  SOCKET_RECONNECT_ATTEMPTS: 5,
  SOCKET_RECONNECT_DELAY: 1000,
};
export default config;
