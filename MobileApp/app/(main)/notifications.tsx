import { Colors } from "@/constants/Colors";
import { Container } from "@/shared/SharedStyles";
import { ScrollView, StyleSheet, Text, useColorScheme, View } from "react-native";

export default function NotiScreen() {
    const colorScheme = useColorScheme();
    const check = colorScheme ?? "light";

    return (
        <>
            <ScrollView
                style={[
                    Container.base,
                    {
                        backgroundColor: Colors[check].background,
                    }
                ]}
                contentContainerStyle={[
                    Container.baseContent
                ]}
            >
                
            </ScrollView>
        </>
    )
}
