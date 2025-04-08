import React, { ReactNode } from 'react';
import {
  ScrollView,
  ScrollViewProps,
  RefreshControl,
  KeyboardAvoidingView,
  Platform,
  StyleSheet,
  View,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { BaseColors } from '@/constants/Colors';

interface SafeScrollViewProps extends ScrollViewProps {
  children: ReactNode;
  refreshing?: boolean;
  onRefresh?: () => void;
  keyboardAvoiding?: boolean;
  safeBottom?: boolean;
  safeTop?: boolean;
  backgroundColor?: string;
  contentContainerStyle?: object;
}

/**
 * A safe area aware ScrollView that handles keyboard avoiding and pull-to-refresh
 */
const SafeScrollView: React.FC<SafeScrollViewProps> = ({
  children,
  refreshing = false,
  onRefresh,
  keyboardAvoiding = true,
  safeBottom = true,
  safeTop = true,
  backgroundColor = BaseColors.dark_pri,
  contentContainerStyle,
  ...props
}) => {
  const insets = useSafeAreaInsets();
  
  const containerStyle = {
    backgroundColor,
    flex: 1,
  };

  const contentStyle = {
    flexGrow: 1,
    paddingBottom: safeBottom ? insets.bottom : 0,
    paddingTop: safeTop ? insets.top : 0,
    ...contentContainerStyle,
  };

  const scrollViewContent = (
    <ScrollView
      bounces={!!onRefresh}
      refreshControl={
        onRefresh ? (
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={BaseColors.primary}
            colors={[BaseColors.primary]}
          />
        ) : undefined
      }
      showsVerticalScrollIndicator={false}
      contentContainerStyle={contentStyle}
      style={styles.scrollView}
      {...props}
    >
      {children}
    </ScrollView>
  );

  if (keyboardAvoiding && Platform.OS === 'ios') {
    return (
      <View style={containerStyle}>
        <KeyboardAvoidingView
          style={styles.keyboardAvoid}
          behavior="padding"
          keyboardVerticalOffset={10}
        >
          {scrollViewContent}
        </KeyboardAvoidingView>
      </View>
    );
  }

  return <View style={containerStyle}>{scrollViewContent}</View>;
};

const styles = StyleSheet.create({
  scrollView: {
    flex: 1,
  },
  keyboardAvoid: {
    flex: 1,
  },
});

export default SafeScrollView;