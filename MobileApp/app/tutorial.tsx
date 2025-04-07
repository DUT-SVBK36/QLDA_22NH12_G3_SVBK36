import SafeScreen from "@/components/layout/SafeScreen";
import { Container } from "@/shared/SharedStyles";
import { Image, StyleSheet, Text } from "react-native";


interface TutorialData {
    id: string;
    title: string;
    description: string;
    image: string | any;
}

export default function TutorialScreen() {
    const tutorialData: TutorialData[] = [
        
    ]


    return (
        <>
            <SafeScreen style={[
                Container.base,
                Container.baseContent,
                styles.container
            ]}>
                <Text>Hello</Text>
                <Image

                    style={styles.image}
                />
            </SafeScreen>  
        </>
    );
}
const styles = StyleSheet.create({
    container: {

    },
    image: {
        minHeight: 288,
        minWidth: 288,
    }
})