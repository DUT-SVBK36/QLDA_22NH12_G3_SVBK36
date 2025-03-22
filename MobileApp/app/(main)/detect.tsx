import CustomButton from "@/components/ui/CustomButton";
import { BaseColors } from "@/constants/Colors";
import SharedAssets from "@/shared/SharedAssets";
import { Container, Fonts } from "@/shared/SharedStyles";
import { useState } from "react";
import { ImageBackground, ScrollView, StyleSheet, Text, View} from "react-native";



export default function DetectScreen(){
    const [camera, hasCamera] = useState<boolean>(false);
    return (
        <>
            <ImageBackground 
            source={SharedAssets.Bg}
            resizeMode="cover"
            style={{
                width: "100%",
                height: "100%",
                position: "absolute",
            }}
            />
            <ScrollView style={[
                Container.base

            ]}
                contentContainerStyle={[
                    Container.baseContent,
                ]}
            >
                <Text
                    style={[
                        Fonts.h1,
                        styles.title
                    ]}
                >
                    Detect
                </Text>
                <View style={styles.cameraContainer}>
                    <Text style={{
                        ...Fonts.body,
                        color: BaseColors.white,

                    }}>
                        No camera Feed
                    </Text>
                </View>
                <CustomButton
                    variant="red"
                    label="Connect"
                    onPress={() => alert('connect')}
                />
            </ScrollView>
        </>
    )
}
const styles = StyleSheet.create({
    title: {
        color: BaseColors.dark_pri,
        textAlign: "left",
        width: "100%",
        marginBottom: 12
    },
    cameraContainer: {
        width: "100%",
        height: 300,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: BaseColors.dark_pri,
        borderRadius: 5,
    }

})