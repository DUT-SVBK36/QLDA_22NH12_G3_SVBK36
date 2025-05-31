import { BaseColors } from "@/constants/Colors"
import { Fonts } from "@/shared/SharedStyles"
import { Ionicons } from "@expo/vector-icons"
import { Text, TouchableOpacity } from "react-native"
import styles from "./styles.css";

interface IconBtnProps {
    onPress: () => void;
    label: string;
    icon: any;
    borderColor?: string;
}

const IconBtn = (
    { onPress, label, icon, borderColor }: IconBtnProps
) => {
    return (
         <TouchableOpacity 
          style={[styles.container, 
            borderColor &&
            { 
                borderLeftWidth: 4,
                borderLeftColor: borderColor, 
            }]}
          onPress={onPress}
        >
          <Ionicons
            name={icon}
            size={24}
            color={BaseColors.white}
          />
          <Text
            style={[
              Fonts.body,
              {
                color: BaseColors.white,
                // textAlign: "center",
                paddingVertical: 8,
                // width: "100%",
              }
            ]}
          >
            {label}
          </Text>
        </TouchableOpacity>
    )
}

export default IconBtn