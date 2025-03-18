import { router } from "expo-router";
import { Text, Touchable, TouchableOpacity, View } from "react-native";

export default function DetectScreen(){
    return (
        <View style={{flex: 1, justifyContent: 'center', alignItems: 'center'}}>
            <Text>detect</Text>
            <TouchableOpacity onPress={() => router.push('/login')}>
                <Text style={{
                    color: 'white'
                }}>To Login</Text>
            </TouchableOpacity>
        </View>
    )
}