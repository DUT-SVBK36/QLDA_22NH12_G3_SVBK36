import { useLocalSearchParams } from "expo-router";
import { Text, View } from "react-native";

export default function SessionItem(){
    const { id } = useLocalSearchParams<{ id: string }>();
    return (
        <View >
            <Text>Session Item</Text>
            {/* Add more UI elements as needed */}
        </View>
    )
}