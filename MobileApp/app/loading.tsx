import { Image, StyleSheet, View } from "react-native";
import SharedAssets from "@/shared/SharedAssets";
export default function LoadingPage() {
    return (
        <View style={styles.container}>
            <Image
                source={SharedAssets.Logo}
                style={{
                    width: 200,
                    height: 200,
                    resizeMode: "contain",
                }}
            />
        </View>
    )
}
const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#282c4d",
    },
}); 