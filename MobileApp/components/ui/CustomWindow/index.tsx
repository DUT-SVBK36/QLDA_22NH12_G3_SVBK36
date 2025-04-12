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
    scrollable?: boolean;
}

export default function CustomWindow(
    { 
        title = "Custom Window", 
        children,
        containerStyle,
        contentContainerStyle,
        maxHeight, // Add a maxHeight prop for better control
        scrollable = true
    }: CustomWindowProps
) {
    const ContentWrapper = scrollable ? ScrollView : View;

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
            <ContentWrapper 
                style={[
                    styles.content,
                    maxHeight ? { maxHeight } : null,
                ]}
                contentContainerStyle={scrollable ? [
                    styles.contentContainer,
                    contentContainerStyle,
                ] : undefined}
                showsVerticalScrollIndicator={scrollable}
            >
                {children}
            </ContentWrapper>
        </View>
    );
}