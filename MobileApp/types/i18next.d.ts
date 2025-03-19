import 'i18next';

// Extend i18next typings
declare module 'i18next' {
  interface InitOptions {
    compatibilityJSON?: string;
  }
  
  interface ReactOptions {
    useSuspense?: boolean;
  }
}