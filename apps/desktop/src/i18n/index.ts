/**
 * i18n (Internationalization) setup for ClipShot.
 * 
 * Uses react-i18next with ICU MessageFormat for professional translations.
 */

import i18next from 'i18next';
import { initReactI18next } from 'react-i18next';
import ICU from 'i18next-icu';

// Import translations
import enCommon from './locales/en/common.json';
import enUI from './locales/en/ui.json';
import trCommon from './locales/tr/common.json';
import trUI from './locales/tr/ui.json';
import deCommon from './locales/de/common.json';
import deUI from './locales/de/ui.json';
import esCommon from './locales/es/common.json';
import esUI from './locales/es/ui.json';
import frCommon from './locales/fr/common.json';
import frUI from './locales/fr/ui.json';

export interface SupportedLocale {
  code: string;
  name: string;
  nativeName: string;
  dir: 'ltr' | 'rtl';
}

// Supported languages
export const SUPPORTED_LOCALES: SupportedLocale[] = [
  { code: 'en', name: 'English', nativeName: 'English', dir: 'ltr' },
  { code: 'tr', name: 'Turkish', nativeName: 'Türkçe', dir: 'ltr' },
  { code: 'de', name: 'German', nativeName: 'Deutsch', dir: 'ltr' },
  { code: 'fr', name: 'French', nativeName: 'Français', dir: 'ltr' },
  { code: 'es', name: 'Spanish', nativeName: 'Español', dir: 'ltr' },
];

// Default namespace
const DEFAULT_NS = 'common';

// All core namespaces
const NAMESPACES = ['common', 'ui'];

// Initialize i18n
export async function initI18n(): Promise<typeof i18next> {
  await i18next
    .use(ICU)
    .use(initReactI18next)
    .init({
      fallbackLng: 'en',
      defaultNS: DEFAULT_NS,
      ns: NAMESPACES,
      
      // Resources
      resources: {
        en: {
          common: enCommon,
          ui: enUI,
        },
        tr: {
          common: trCommon,
          ui: trUI,
        },
        de: {
          common: deCommon,
          ui: deUI,
        },
        es: {
          common: esCommon,
          ui: esUI,
        },
        fr: {
          common: frCommon,
          ui: frUI,
        },
      },
      
      // Namespace separator
      nsSeparator: ':',
      keySeparator: '.',
      
      // Detection
      lng: localStorage.getItem('clipshot_language') || 'en',
      
      // Interpolation
      interpolation: {
        escapeValue: false, // React already escapes
      },
      
      // ICU format options
      icu: {
        memoize: true,
      },
      
      // React specific
      react: {
        useSuspense: false,
      },
    });
  
  return i18next;
}

export { i18next };
export default i18next;
