import React from "react";
import { View, Text, Image, useColorScheme, TouchableOpacity } from "react-native";
import { styles } from "./style.css";
import { Colors } from "@/constants/Colors";
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';
import { faArrowRight } from '@fortawesome/free-solid-svg-icons';
import { Fonts } from "@/shared/SharedStyles";

interface MenuUserProps {
    username?: string;
    onPress?: () => void;
}

const MenuUser = ({
    username = "UserName",
    onPress = () => { console.log("User Menu Pressed")}
}: MenuUserProps
) => {
    const colorScheme = useColorScheme();
    const check = colorScheme ?? "light";
    const textColor = { color: Colors[check].text };
    
    return (
        <TouchableOpacity style={styles.container} onPress={() => {
            onPress();
            console.log("User Menu Pressed");
        }}>
            <Image
                source={require('../../../assets/images/default.jpg')} 
                style={styles.avatar} 
                resizeMode="cover"
            />
            <View style={styles.userInfo}>
                <Text style={[styles.username, textColor, Fonts.subtitle]}>{username}</Text>
                <View style={styles.badge}>
                    <Text style={[styles.badgetext, Fonts.caption]}>Beginner</Text>
                </View>
            </View>
            <View style={styles.rightContainer}>
                <FontAwesomeIcon 
                    icon={faArrowRight} 
                    size={20} 
                    color={Colors[check].text}
                />
            </View>
        </TouchableOpacity>
    );
};

export default MenuUser;