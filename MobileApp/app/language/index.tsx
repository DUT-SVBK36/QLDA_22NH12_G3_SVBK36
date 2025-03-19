import { Fonts } from "@/shared/SharedStyles";
import { memo } from "react";
import { Text, TouchableOpacity } from "react-native";

interface LanguageOptProps {
    lang: string;
    onPress: () => void;
}


export default function LanguageScreen() {

    return (
        <>
            <Text>Language</Text>
        </>
    )
}
