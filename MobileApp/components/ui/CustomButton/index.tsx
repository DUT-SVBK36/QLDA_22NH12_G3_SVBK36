import { TouchableOpacity, Text, useColorScheme } from "react-native";
import styles from "./styles.css";
import { Colors } from "@/constants/Colors";
import { Fonts } from "@/shared/SharedStyles";

interface CustomButtonProps {
    onPress: () => void;
    label: string;
    variant?: 'default' | 'orange' | 'red' | 'blue';
}
const StdBtnVariant = {
    orange: '#CA5618',
    red: '#9F1719',
    blue: '#0078D4',
}
export default function CustomButton( { onPress, label, variant = 'default' }: CustomButtonProps){    
    const colorScheme = useColorScheme();
    const check = variant === 'default';
    return (
        <TouchableOpacity style={{
            ...styles.container,
            backgroundColor: check ? Colors[colorScheme ?? "light"].button.bg : StdBtnVariant[variant],
            }} onPress={onPress}>
            <Text style={{
                ...styles.text,
                ...Fonts.semiBold,
                color: check ? Colors[colorScheme ?? "light"].button.tint : '#fff',
            }}>{label}</Text>
        </TouchableOpacity>
    )
}