import React from "react";
import { View, Text, Image, useColorScheme } from "react-native";
import { styles } from "./style.css";
import { Colors } from "@/constants/Colors";
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';
import { faArrowRight } from '@fortawesome/free-solid-svg-icons';
const MenuUser = () => {
    const colorScheme = useColorScheme();
    const check = colorScheme ?? "light";
    const textColor = { color: Colors[check].text };
    
    return (
        <View style={styles.container}>
            <Image
                source={require('../../../assets/images/default.jpg')} 
                style={styles.avatar} 
                resizeMode="cover"
            />
            <View style={styles.userInfo}>
                <Text style={[styles.username, textColor]}>UserName</Text>
                <View style={styles.badge}>
                <Text style={styles.badgetext}>Beginner</Text>
                </View>
                
            </View>
            <View style={styles.rightContainer}>
                <FontAwesomeIcon 
                    icon={faArrowRight} 
                    size={20} 
                    color={Colors[check].text}
                />
            </View>
        </View>
    );
};

export default MenuUser;