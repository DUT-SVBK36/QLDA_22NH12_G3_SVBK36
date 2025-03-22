import { Image, ImageProps, Text, View } from "react-native";
import styles from "./styles.css";
import * as Progress from 'react-native-progress';
import { BaseColors } from "@/constants/Colors";
import SharedAssets from "@/shared/SharedAssets";
import { Fonts } from "@/shared/SharedStyles";
interface UserCardProps {
    profilePic?: string | any;
    username?: string;
    currentLevel?: number;
    currentPoints?: number;
    onPress?: () => void;
}

/**
 * UserCard component displays a user's profile information.
 * 
 * @component
 * @param {Object} props - The component props
 * @param {ImageSourcePropType} [props.profilePic] - The user's profile picture (defaults to default avatar)
 * @param {string} [props.username="Sample User"] - The user's display name
 * @param {number} [props.currentLevel=10] - The user's current level
 * @param {number} [props.currentPoints=50] - The user's current points (out of 100 for progress bar)
 * @param {() => void} [props.onPress] - Function to call when card is pressed
 * @returns {JSX.Element} Rendered UserCard component
 */

export default function UserCard(
    {
        profilePic = SharedAssets.defaultAvatar, 
        username = "Sample User", 
        currentLevel = 10, 
        currentPoints = 50, 
        onPress = () => {
            console.log('UserCard Clicked');
        }

    }: UserCardProps
): JSX.Element{
    return (
        <>
            <View style={[styles.container]}
                onTouchEnd={onPress}
            >
                <Image 
                    style={styles.avatar}
                    source={profilePic}
                />
                <View style={[styles.contentHolder]}>
                    <Text style={[
                        Fonts.body,
                        {color: BaseColors.white}
                    ]}>
                        {username}
                    </Text>
                    <View style={[styles.level]}>
                        <Text style={[
                            Fonts.caption,
                            {color: BaseColors.white}
                        ]}
                        >
                            Lvl.{currentLevel}
                        </Text>
                            <Progress.Bar
                                width={null}
                                progress={currentPoints / 100}
                                color={BaseColors.quaternary}
                            />
                    </View>
                </View>
            </View>
        </>
    )
}