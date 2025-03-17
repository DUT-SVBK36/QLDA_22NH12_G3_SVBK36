import { Text, View, TextInput } from "react-native";
import CustomInputCss from "./styles.css";

export default function CustomInput(){
    return (
        <View style={CustomInputCss.container}>
            <Text style={CustomInputCss.label}>Label</Text>
            <TextInput style={CustomInputCss.input} />
        </View>
    )
}