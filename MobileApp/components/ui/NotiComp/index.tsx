import { Colors } from "@/constants/Colors";
import { Fonts } from "@/shared/SharedStyles";
import { FontAwesome5, Ionicons } from "@expo/vector-icons";
import { Alert, Text, TouchableOpacity, useColorScheme, View } from "react-native";
import styles from "./style.css";
import { getTimeAgo } from "@/utils/time-cal";
import { truncateText } from "@/utils/long-text-handler";


interface NotiCompProps {
    title?: string;
    description?: string;
    timeStamps?: Date | number | string;
    onPress?: () => void;
}

export default function NotiComp(
    {
        title = "Sample Title",
        description = "Sample Description",
        timeStamps = Date.now(),
        onPress = () => {
            Alert.alert('Notification Clicked');
        }
    }: NotiCompProps
) {
    //theme detect
    const colorScheme = useColorScheme();
    const check = colorScheme ?? "light";

    //time calculation
    const calculatedTime = getTimeAgo(timeStamps);

    return (
        <>
            <TouchableOpacity style={[
                styles.container
            ]}
            onPress={onPress}
            >
                <FontAwesome5 
                name="exclamation-circle" 
                size={48} 
                color={Colors[check].text} 
                />
                <View
                    style={[
                        styles.contentHolder
                    ]}
                >
                    <Text
                        style={[
                            Fonts.body,
                            {color: Colors[check].text}
                        ]}
                    >
                        {title}
                    </Text>

                    <Text
                    style={[
                        Fonts.caption,
                        {color: Colors[check].text}
                    ]}
                    >
                        {truncateText(description, 30, "...")}
                    </Text>

                    <Text
                        style={[
                            Fonts.small,
                            styles.timeStampsTint
                        ]}
                    >
                        {calculatedTime}
                    </Text>
                </View>
            </TouchableOpacity>
        </>
    )
}