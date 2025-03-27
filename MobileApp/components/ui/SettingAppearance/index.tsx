import React, { useState } from 'react';
import { View, Text, Switch } from 'react-native';
import { useColorScheme } from 'react-native';
import { Colors } from '@/constants/Colors';
import { Fonts } from '@/shared/SharedStyles';
import { styles } from './style.css';

const SettingAppearance = () => {
    const colorScheme = useColorScheme();
    const check = colorScheme ?? 'light';
    const textColor = { color: Colors[check].text };

    // State để lưu trạng thái của switch
    const [darkMode, setDarkMode] = useState(false);
    const [notifications, setNotifications] = useState(false);

    return (
        <View style={styles.section}>
            
            <View style={styles.switchs}>
                <Text style={[styles.label, textColor, Fonts.body]}>Dark mode</Text>
                <Switch 
                    value={darkMode} 
                    onValueChange={setDarkMode}
                    trackColor={{ false: '#767577', true: Colors[check].tint }}
                />
            </View>

            <View style={styles.switchs}>
                <Text style={[styles.label, textColor, Fonts.body]}>Receive notification</Text>
                <Switch 
                    value={notifications} 
                    onValueChange={setNotifications} 
                    trackColor={{ false: '#767577', true: Colors[check].tint }}
                />
            </View>
        </View>
    );
};

export default SettingAppearance;