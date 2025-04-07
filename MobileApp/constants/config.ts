const config = {
    BASE_URL: 'http://192.168.1.69:8000/',
    API_URL: 'http://192.168.1.69:8000/api/v1',
    CAMERA_URL: 'http://192.168.101.3',

    //Socket configuration
    SOCKET_URL: 'ws://192.168.1.69:8000/api/v1/ws/detect',
    SOCKET_RECONNECT_ATTEMPTS: 5,
    SOCKET_RECONNECT_DELAY: 1000,

}
export default config;