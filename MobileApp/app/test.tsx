import CustomInput from "@/components/CustomInput";
import { View } from "react-native";

export default function Test(){
    return (
        <View style={{
            flex: 1,
            justifyContent: 'center',
            alignItems: 'center',
            backgroundColor: '#282c4d',
            paddingHorizontal: 16,
        }}>
            <CustomInput />
        </View>
    )
}