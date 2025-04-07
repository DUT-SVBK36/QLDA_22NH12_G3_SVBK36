import { ActivityIndicator, Image, Text, View } from "react-native";
import styles from "./styles.css";
import { BaseColors } from "@/constants/Colors";
import { Fonts } from "@/shared/SharedStyles";
import React, { useEffect, useState } from "react";
import config from "@/constants/config";
import Video from 'react-native-video';
import WebView from "react-native-webview";

interface CameraFeedProps {
    cameraIp?: string,
    isDetecting: boolean,

}
export default function CameraFeed({ 
    cameraIp = config.CAMERA_URL + "/capture",
    isDetecting = true
}: CameraFeedProps) {
    const [isCameraConnected, setIsCameraConnected] = useState(true);
    const [imageUrl, setImageUrl] = useState<string | null>(null);
    //check if camera is connected
    const cameraCheck = async () => {
        try {
            // debugger;
            const response = await fetch(cameraIp);
            if (response.ok) {
                setIsCameraConnected(true);
            } else {
                setIsCameraConnected(false);
            }
        } catch (error) {
            console.error("Error checking camera status:", error);
            setIsCameraConnected(false);
        }
    }

    //capture and send frame to server
    const captureAndSendFrame = async () => {
        // debugger;
        console.log('capture');
    }

    //check if camera is connected every 5 seconds
    // useEffect(() => {
    //     const checkCamera = async () => {
    //         await cameraCheck();
    //     };

    //     const interval = setInterval(() => {
    //         checkCamera();
    //     }, 5000); // Check every 5 seconds
    //     return () => clearInterval(interval); // Cleanup on unmount

    // }, [])

    useEffect(() => {
        const interval = setInterval(() => {
            setImageUrl(cameraIp + "?t=" + new Date().getTime());
        }, 500);
        return () => clearInterval(interval); // Cleanup on unmount
    }, [])


    return (
        <View style={styles.cameraContainer}>
            {isCameraConnected ? 
            <>
                <Image
                    source={{ uri: imageUrl as string }}
                    style={styles.cameraContainer}
                    resizeMode="cover"
                />
            </>
            :
            <Text style={{
                ...Fonts.body,
                color: BaseColors.white,
            }}>
                No camera Feed
            </Text>
            }
            
        </View>
    )
}