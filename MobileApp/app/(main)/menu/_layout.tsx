import { Colors } from '@/constants/Colors';
import { Stack } from 'expo-router';
import { useColorScheme } from 'react-native';

export default function MenuLayout() {
    const colorScheme = useColorScheme();

    return (
        <Stack
            screenOptions={{
                headerStyle: {
                    backgroundColor: Colors[colorScheme ?? 'light'].background,
                },
                headerTintColor: Colors[colorScheme ?? 'light'].text,
                headerTitleStyle: {
                    fontWeight: 'bold',
                },
                headerShadowVisible: false,
            }}
        >
            <Stack.Screen
                name="index"
                options={{
                    headerShown: false,
                }}
            />
            <Stack.Screen
                name="me"
                options={{
                    headerShown: true,
                    title: 'Dashboard',
                }}
            />
            <Stack.Screen
                name="setting"
                options={{
                    // headerShown: false,
                    title: '',
                    headerStyle: {
                        backgroundColor: Colors[colorScheme ?? 'light'].background,
                    },
                    headerTintColor: Colors[colorScheme ?? 'light'].text,
                }}
            />
            <Stack.Screen
                name="history"
                options={{
                    headerShown: false,
                }}
            />
            <Stack.Screen
                name="session"
                options={{
                    headerShown: false,
                }}
            />
            
            {/* session-item?id=<id> */}
            <Stack.Screen
                name="session-item"
                options={{
                    headerShown: false,
                    presentation: 'modal',
                }}
            />
        </Stack>
    );
}