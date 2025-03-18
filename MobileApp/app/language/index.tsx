import { Fonts } from "@/shared/SharedStyles";
import { memo } from "react";
import { Text, TouchableOpacity } from "react-native";

interface LanguageOptProps {
    lang: string;
    onPress: () => void;
}


export default function LanguageScreen() {
    const languageOpt = memo(({lang, onPress} : LanguageOptProps) => {
        return (
            <TouchableOpacity style={{
                borderBottomColor: '#fff',
                borderBottomWidth: 1,
                padding: 10,
            }}
                onPress={onPress}
            >
                <Text
                style={[
                    Fonts.bodySmall
                ]}
                >{lang}</Text>
            </TouchableOpacity>
        )
    });

    return (
        <>
            <Text>Language</Text>
        </>
    )
}
