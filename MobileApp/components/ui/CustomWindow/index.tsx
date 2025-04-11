import { ScrollView, Text, ViewStyle } from "react-native";
import { View } from "react-native";
import styles from "./styles.css";
import { Fonts } from "@/shared/SharedStyles";

interface CustomWindowProps {
    title?: string;
    children?: React.ReactNode;
    containerStyle?: ViewStyle;
    contentContainerStyle?: ViewStyle;
    maxHeight?: number;
}

export default function CustomWindow(
    { 
        title = "Custom Window", 
        children,
        containerStyle,
        contentContainerStyle,
        maxHeight // Add a maxHeight prop for better control
    }: CustomWindowProps
) {
    return (
        <View style={[
            styles.container,
            containerStyle
        ]}>
            <View style={[
                styles.titleBar
            ]}>
                <Text style={[
                    Fonts.bodySmall,
                    styles.title,
                ]}>
                    {title}
                </Text>
            </View>
            <ScrollView 
                style={[
                    styles.content,
                    maxHeight ? { maxHeight } : null,
                ]}
                contentContainerStyle={[
                    styles.contentContainer,
                    contentContainerStyle,
                ]}
                showsVerticalScrollIndicator={true}
            >
                {children}
            </ScrollView>
        </View>
    );
}