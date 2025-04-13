import { Image, Text, TouchableOpacity, View } from "react-native";
import styles from "./styles.css";
import { Fonts } from "@/shared/SharedStyles";
import { FontAwesome5 } from "@expo/vector-icons";
import config from "@/constants/config";
import { useState } from "react";

interface WrongPostureCardProps {
    id?: string;
    client?: string;
    image?: any;
    detectedPosture?: string;
    accuracy?: number;
    desc?: string;
    timestamp?: string;
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
    const [isExpanded, setIsExpanded] = useState(false);
    return (
        <>
            <TouchableOpacity style={[
                styles.container
            ]}
            onPress={() => {
                setIsExpanded(!isExpanded);
            }}
            >
                <Image
                    source={{
                        uri: `${image}`
                    }}
                    style={[
                        styles.img,
                        isExpanded && {
                            flex: 1,
                            height: "100%",
                            objectFit: "cover",
                        }
                    ]}
                />
                <View style={[
                    styles.content
                ]}>
                    <Text style={[
                        Fonts.caption,
                        styles.titleTint
                    ]}>
                        {detectedPosture} 
                        {/* ({(accuracy * 100).toFixed(2)}%) */}
                    </Text>
                    <Text style={[
                        Fonts.caption,
                        styles.tint,
                        { marginBottom: 4}
                    ]}>
                        Acc: {(accuracy * 100).toFixed(2)}%
                    </Text>
                    <Text style={[
                        Fonts.small,
                        styles.tint,
                    ]}>
                        <FontAwesome5 
                            name="clock" 
                            size={10} 
                            color={"white"}
                        />  {new Date(timestamp).toLocaleString("vi-VN", { hour12: false })}
                    </Text>
                </View>
            </TouchableOpacity>
        </>
    )
}