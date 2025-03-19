import BackgroundView from "@/components/layout/BackgroundView";
import CustomButton from "@/components/ui/CustomButton";
import SharedAssets from "@/shared/SharedAssets";
import { Text, View } from "react-native";



export default function DetectScreen(){
    return (
        <BackgroundView
            customBackground={SharedAssets.Bg}
        >
            <View>
                <Text>Camera</Text>
            </View>
            <CustomButton
                variant="orange"
                label="Connect"
                onPress={() => alert('connect')}
            />
        </BackgroundView>
    )
}