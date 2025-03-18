import CustomButton from "@/components/ui/CustomButton";
import CustomInput from "@/components/ui/CustomInput";
import { useState } from "react";
import { View } from "react-native";

export default function Test(){
    const [text, setText] = useState('');
    return (
        <View style={{
            flex: 1,
            justifyContent: 'center',
            alignItems: 'center',
            backgroundColor: '#282c4d',
            paddingHorizontal: 16,
        }}>
            <CustomInput
                type={"emailAddress"}
                label="Email"
                value={text}
                onChangeText={setText}
                placeholder="Enter your email"
                isPassword={false}
            />
            <CustomButton 
                variant="orange"
                label="Submit"
                onPress={() => alert(text)}
            />
        </View>
    )
}