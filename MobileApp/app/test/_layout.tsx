import ProtectedRoute from "@/components/auth/ProtectedRoute";
import { Colors } from "@/constants/Colors";
import { Stack } from "expo-router";
import { useColorScheme } from "react-native";

export default function TestLayout(){
    const colorScheme = useColorScheme();
    return (
        <ProtectedRoute>
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
                    name="socket"
                    options={{
                        headerShown: true,
                    }}
                />
        
            </Stack>
        </ProtectedRoute>
    )
}