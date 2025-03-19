import { Text, View, TextInput, useColorScheme } from "react-native";
import styles from "./styles.css";
import { Colors } from "@/constants/Colors";

type textContentType = 
    | 'none'
    | 'URL'
    | 'addressCity'
    | 'addressCityAndState'
    | 'addressState'
    | 'countryName'
    | 'creditCardNumber'
    | 'creditCardExpiration'
    | 'creditCardExpirationMonth'
    | 'creditCardExpirationYear'
    | 'creditCardSecurityCode'
    | 'creditCardType'
    | 'creditCardName'
    | 'creditCardGivenName'
    | 'creditCardMiddleName'
    | 'creditCardFamilyName'
    | 'emailAddress'
    | 'familyName'
    | 'fullStreetAddress'
    | 'givenName'
    | 'jobTitle'
    | 'location'
    | 'middleName'
    | 'name'
    | 'namePrefix'
    | 'nameSuffix'
    | 'nickname'
    | 'organizationName'
    | 'postalCode'
    | 'streetAddressLine1'
    | 'streetAddressLine2'
    | 'sublocality'
    | 'telephoneNumber'
    | 'username'
    | 'password'
    | 'newPassword'
    | 'oneTimeCode'
    | 'birthdate'
    | 'birthdateDay'
    | 'birthdateMonth'
    | 'birthdateYear'
    | undefined;

interface CustomInputProps {
    type?: textContentType;
    label: string;
    value: string;
    onChangeText: (text: string) => void;
    placeholder: string;
    isPassword?: boolean;
}
export default function CustomInput( 
    {type, label, value, onChangeText, placeholder, isPassword }
    : CustomInputProps
){
    const colorScheme = useColorScheme();
    return (
        <View style={[
            styles.container,
            {borderBottomColor: Colors[colorScheme ?? 'light'].text,}

        ]}>
            <Text style={[
                styles.label,
                {color: Colors[colorScheme ?? 'light'].text,}
                ]}>{label}</Text>
            <TextInput style={[
                styles.input,
                {color: Colors[colorScheme ?? 'light'].text,}
            ]} 
                textContentType={type}
                value={value}
                onChangeText={onChangeText}
                placeholder={placeholder}
                placeholderTextColor={colorScheme === 'dark' ? 'gray' : 'black'}
                autoCapitalize="none"
                autoCorrect={false}
                secureTextEntry={isPassword}
            />
        </View>
    )
}