import React from "react";
import { View, Text, TouchableOpacity, useColorScheme } from "react-native";
import { styles } from "./style.css";
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';
import { 
    faGlobe, 
    faCheckCircle, 
    faHistory, 
    faGear, 
    faInfo, 
    faRightFromBracket, 
    faExplosion
} from '@fortawesome/free-solid-svg-icons';
import { Colors } from "@/constants/Colors";
import { Fonts } from "@/shared/SharedStyles";

interface MenuOptionProps {
        icon: keyof typeof IconMap;
        label: string;
        onPress?: () => void;
}

const IconMap = {
        'test': faExplosion,
        'globe': faGlobe,
        'check-circle': faCheckCircle,
        'history': faHistory,
        'settings': faGear,
        'info': faInfo,
        'log-out': faRightFromBracket
};

const MenuOption: React.FC<MenuOptionProps> = ({ icon, label, onPress }) => {
        const iconDef = IconMap[icon];
        const colorScheme = useColorScheme();
        const check = colorScheme ?? "light";
        const textColor = { color: Colors[check].text };
        return (
                <TouchableOpacity style={styles.container} onPress={onPress}>
                        <View style={styles.iconContainer}>
                                <FontAwesomeIcon 
                                        icon={iconDef} 
                                        size={24} 
                                        color= {Colors[check].text}
                                />
                        </View>
                        <Text style={[styles.label, Fonts.body, textColor]}>{label}</Text>
                </TouchableOpacity>
        );
};

export default MenuOption;