import { FontAwesomeIcon } from "@fortawesome/react-native-fontawesome";
import { Text, View } from "react-native";
import CustomButton from "../../CustomButton";
import styles from "./styles.css";
import { Ionicons } from "@expo/vector-icons";
import { Fonts } from "@/shared/SharedStyles";
import { useRouter } from "expo-router";

interface RecentSessionProps {
    timeStamp?: string;
    fails?: number;
}
export default function RecentSession(
    {
        timeStamp = "2023-10-01 12:00:00",
        fails = 12,
    }: RecentSessionProps
) {
    const router = useRouter();
  return (
    <>
        <View style={[
            styles.container
        ]}>
            <View style={[
                styles.content
            ]}>
                <Ionicons 
                    name="timer-outline"
                    size={48}
                    color="white"
                />
                <View style={[
                    styles.textContent
                ]}>
                    <Text
                        style={[
                            Fonts.bodySmall,
                            {color: "white"}
                        ]}
                    >Recent: {timeStamp}</Text>
                    {fails > 0 
                    && 
                    <Text
                    style={[
                        Fonts.bodySmall,
                        {
                            color: "white",
                            
                        }
                    ]}
                    >{`Fails: ${fails}`}</Text>}
                </View>
            </View>
            <CustomButton 
                label="View history"
                onPress={() => {
                    router.push("/(main)/menu/history")
                }}
                variant="blue"
            />
        </View>
    </>
  );
}