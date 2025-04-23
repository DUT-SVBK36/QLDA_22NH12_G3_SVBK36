import { Image, Text, TouchableOpacity, View } from "react-native";
import styles from "./styles.css";
import { Fonts } from "@/shared/SharedStyles";
import { FontAwesome5, Ionicons } from "@expo/vector-icons";
import config from "@/constants/config";
import { useState } from "react";
import { usePopupStore } from "@/services/popup";
import { PostureMappedString } from "@/utils/postures-map";

interface WrongPostureCardProps {
    id?: string;
    client?: string;
    image?: any;
    detectedPosture?: string;
    accuracy?: number;
    desc?: string;
    timestamp?: string;
    event? : () => void;
}

export default function WrongPostureCard(
    {
        id = "12345678-1234-1234-1234-123456789012",
        client = "detect",
        image = "https://placehold.co/600x400",
        detectedPosture = "Wrong Posture",
        accuracy = 0.96,
        desc = "Adjust your posture",
        timestamp = new Date().toLocaleString("vi-VN", { hour12: false })
    }: WrongPostureCardProps
) {
    const { showPopup } = usePopupStore();
    const [isExpanded, setIsExpanded] = useState(false);
    return (
        <>
            <TouchableOpacity style={[
                styles.container
            ]}
            onPress={() => showPopup({
                image: image,
                label_name: detectedPosture,
                accuracy: accuracy,
                timestamp: timestamp,
                label_recommendation: desc
              })}
              activeOpacity={0.7}
            >
                <Ionicons 
                    name="image"
                    size={24}
                    color={"black"}
                />
                <View style={[
                    styles.content
                ]}>
                    <Text style={[
                        Fonts.caption,
                        styles.titleTint
                    ]}>
                        {PostureMappedString[detectedPosture]} 
                        {/* ({(accuracy * 100).toFixed(2)}%) */}
                    </Text>
                    {/* <Text style={[
                        Fonts.caption,
                        styles.tint,
                        { marginBottom: 4}
                    ]}>
                        Acc: {(accuracy * 100).toFixed(2) + 60}%
                    </Text> */}
                    <Text style={[
                        Fonts.small,
                        styles.tint,
                    ]}>
                        <FontAwesome5 
                            name="clock" 
                            size={10} 
                            color={"black"}
                        />  {new Date(timestamp).toLocaleString("vi-VN", { hour12: false })}
                    </Text>
                </View>
            </TouchableOpacity>
        </>
    )
}