import NotiComp from "@/components/ui/NotiComp";
import { Colors } from "@/constants/Colors";
import { Container, Fonts } from "@/shared/SharedStyles";
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
                <Text
                      style={[
                        Container.title,
                        Fonts.h1Large,
                        {color: Colors[check].text}
                ]}
                >
                    Notifications
                </Text>

                <NotiComp 
                description="You have a new notification"
                title="New Notification"
                timeStamps={Date.now()}
                />
                <NotiComp />
                <NotiComp />
                <NotiComp />
            </ScrollView>
        </>
    )
}

const styles = StyleSheet.create({
    
})
