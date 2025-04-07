import { ScrollView, Text } from "react-native";
import { View } from "react-native";
import styles from "./styles.css";
import { Fonts } from "@/shared/SharedStyles";

interface CustomWindowProps {
    title?: string;
    children?: React.ReactNode;
    containerStyle?: object;
    contentContainerStyle?: object;
}
export default function CustomWindow(
    { 
        title = "Custom Window", 
        children,
        containerStyle,
        contentContainerStyle
    }: CustomWindowProps
) {
    return (
        <View style={[
            styles.container,
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
                containerStyle
            ]}
            contentContainerStyle={[
                {justifyContent: 'flex-start'},
                contentContainerStyle,
            ]}
            >
                {children}
            </ScrollView>
        </View>
    );
}