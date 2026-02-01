# 🌍 LOCALIZATION (i18n) — CLIPSHOT

> Uluslararasılaştırma mimarisi, çeviri yapısı ve plugin dil desteği.

---

## 🎯 i18n PRENSİPLERİ

1. **ICU Message Format** — Çoğullama, cinsiyet, koşullar için standart
2. **Lazy Loading** — Sadece aktif dil yüklenir
3. **Plugin Support** — Her plugin kendi çevirilerini getirir
4. **Fallback Chain** — tr-TR → tr → en
5. **RTL Support** — Arapça, İbranice gibi RTL diller desteklenir

---

## 🏗️ MİMARİ

```
┌─────────────────────────────────────────────────────────────────┐
│                         APP LAYER                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    i18n Provider                          │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐         │  │
│  │  │ Core Locale │ │Plugin Locale│ │ User Prefs  │         │  │
│  │  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘         │  │
│  │         │               │               │                 │  │
│  │         └───────────────┴───────────────┘                 │  │
│  │                         │                                 │  │
│  │                    ┌────▼────┐                            │  │
│  │                    │ Merger  │                            │  │
│  │                    └────┬────┘                            │  │
│  │                         │                                 │  │
│  │                    ┌────▼────┐                            │  │
│  │                    │ Cache   │                            │  │
│  │                    └─────────┘                            │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 DOSYA YAPISI

### Core Locales

```
clipshot/
└── apps/
    └── desktop/
        └── src/
            └── locales/
                ├── index.ts           # i18n setup
                ├── loader.ts          # Locale loader
                ├── types.ts           # Type definitions
                │
                ├── en/
                │   ├── common.json    # Shared strings
                │   ├── ui.json        # UI elements
                │   ├── capture.json   # Capture module
                │   ├── ai.json        # AI features
                │   ├── settings.json  # Settings page
                │   ├── marketplace.json # Marketplace
                │   └── errors.json    # Error messages
                │
                ├── tr/
                │   ├── common.json
                │   ├── ui.json
                │   ├── capture.json
                │   ├── ai.json
                │   ├── settings.json
                │   ├── marketplace.json
                │   └── errors.json
                │
                └── [other languages]/
```

### Plugin Locales

```
my-plugin/
└── locales/
    ├── en.json        # English
    ├── tr.json        # Turkish
    └── de.json        # German
```

---

## 📋 LOCALE FILE FORMAT

### ICU Message Format Örnekleri

```json
// locales/en/common.json
{
  "$schema": "https://clipshot.dev/schemas/locale.json",
  
  "app": {
    "name": "ClipShot",
    "tagline": "AI-Powered Gaming Clips"
  },
  
  "actions": {
    "save": "Save",
    "cancel": "Cancel",
    "confirm": "Confirm",
    "delete": "Delete",
    "edit": "Edit",
    "close": "Close"
  },
  
  "time": {
    "seconds": "{count, plural, one {# second} other {# seconds}}",
    "minutes": "{count, plural, one {# minute} other {# minutes}}",
    "hours": "{count, plural, one {# hour} other {# hours}}",
    "ago": "{time} ago",
    "remaining": "{time} remaining"
  },
  
  "files": {
    "size": "{size, number, ::compact-short unit/byte}",
    "count": "{count, plural, =0 {No files} one {# file} other {# files}}"
  },
  
  "notifications": {
    "clipSaved": "Clip saved successfully",
    "clipDeleted": "Clip deleted",
    "exportComplete": "Export complete: {filename}",
    "uploadProgress": "Uploading... {progress, number, ::percent}"
  },
  
  "errors": {
    "generic": "Something went wrong. Please try again.",
    "network": "Network error. Check your connection.",
    "permission": "Permission denied: {permission}",
    "fileNotFound": "File not found: {path}"
  }
}
```

### Turkish Locale

```json
// locales/tr/common.json
{
  "app": {
    "name": "ClipShot",
    "tagline": "Yapay Zeka Destekli Oyun Klipleri"
  },
  
  "actions": {
    "save": "Kaydet",
    "cancel": "İptal",
    "confirm": "Onayla",
    "delete": "Sil",
    "edit": "Düzenle",
    "close": "Kapat"
  },
  
  "time": {
    "seconds": "{count, plural, one {# saniye} other {# saniye}}",
    "minutes": "{count, plural, one {# dakika} other {# dakika}}",
    "hours": "{count, plural, one {# saat} other {# saat}}",
    "ago": "{time} önce",
    "remaining": "{time} kaldı"
  },
  
  "files": {
    "size": "{size, number, ::compact-short unit/byte}",
    "count": "{count, plural, =0 {Dosya yok} one {# dosya} other {# dosya}}"
  },
  
  "notifications": {
    "clipSaved": "Klip başarıyla kaydedildi",
    "clipDeleted": "Klip silindi",
    "exportComplete": "Dışa aktarım tamamlandı: {filename}",
    "uploadProgress": "Yükleniyor... {progress, number, ::percent}"
  },
  
  "errors": {
    "generic": "Bir şeyler ters gitti. Lütfen tekrar deneyin.",
    "network": "Ağ hatası. Bağlantınızı kontrol edin.",
    "permission": "İzin reddedildi: {permission}",
    "fileNotFound": "Dosya bulunamadı: {path}"
  }
}
```

### UI Strings

```json
// locales/en/ui.json
{
  "nav": {
    "home": "Home",
    "clips": "Clips",
    "settings": "Settings",
    "marketplace": "Marketplace",
    "dev": "Developer"
  },
  
  "header": {
    "recording": "Recording",
    "stopped": "Stopped",
    "processing": "Processing..."
  },
  
  "sidebar": {
    "recentClips": "Recent Clips",
    "favorites": "Favorites",
    "allClips": "All Clips",
    "plugins": "Plugins"
  },
  
  "buttons": {
    "startRecording": "Start Recording",
    "stopRecording": "Stop Recording",
    "createClip": "Create Clip",
    "export": "Export",
    "share": "Share"
  },
  
  "labels": {
    "duration": "Duration",
    "quality": "Quality",
    "resolution": "Resolution",
    "fps": "FPS",
    "codec": "Codec",
    "bitrate": "Bitrate"
  },
  
  "placeholders": {
    "search": "Search clips...",
    "title": "Enter title...",
    "description": "Add description..."
  },
  
  "tooltips": {
    "settings": "Open settings",
    "fullscreen": "Toggle fullscreen",
    "mute": "Mute/Unmute",
    "volume": "Volume: {level}%"
  }
}
```

---

## 🔧 i18n IMPLEMENTATION

### Provider Setup

```typescript
// apps/desktop/src/locales/index.ts

import i18next from 'i18next';
import { initReactI18next } from 'react-i18next';
import ICU from 'i18next-icu';
import Backend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

import type { SupportedLocale } from './types';

// Supported languages
export const SUPPORTED_LOCALES: SupportedLocale[] = [
  { code: 'en', name: 'English', nativeName: 'English', dir: 'ltr' },
  { code: 'tr', name: 'Turkish', nativeName: 'Türkçe', dir: 'ltr' },
  { code: 'de', name: 'German', nativeName: 'Deutsch', dir: 'ltr' },
  { code: 'fr', name: 'French', nativeName: 'Français', dir: 'ltr' },
  { code: 'es', name: 'Spanish', nativeName: 'Español', dir: 'ltr' },
  { code: 'ja', name: 'Japanese', nativeName: '日本語', dir: 'ltr' },
  { code: 'ko', name: 'Korean', nativeName: '한국어', dir: 'ltr' },
  { code: 'zh', name: 'Chinese', nativeName: '中文', dir: 'ltr' },
  { code: 'ar', name: 'Arabic', nativeName: 'العربية', dir: 'rtl' },
  { code: 'ru', name: 'Russian', nativeName: 'Русский', dir: 'ltr' },
  { code: 'pt', name: 'Portuguese', nativeName: 'Português', dir: 'ltr' },
];

// Default namespace
const DEFAULT_NS = 'common';

// All core namespaces
const NAMESPACES = ['common', 'ui', 'capture', 'ai', 'settings', 'marketplace', 'errors'];

export async function initI18n(): Promise<typeof i18next> {
  await i18next
    .use(ICU)
    .use(Backend)
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
      fallbackLng: 'en',
      defaultNS: DEFAULT_NS,
      ns: NAMESPACES,
      
      // Namespace separator
      nsSeparator: ':',
      keySeparator: '.',
      
      // Load path for core locales
      backend: {
        loadPath: 'locales/{{lng}}/{{ns}}.json',
      },
      
      // Detection order
      detection: {
        order: ['localStorage', 'navigator', 'htmlTag'],
        caches: ['localStorage'],
        lookupLocalStorage: 'clipshot_language',
      },
      
      // Interpolation
      interpolation: {
        escapeValue: false, // React already escapes
      },
      
      // ICU format options
      icu: {
        memoize: true,
        bindI18n: 'languageChanged',
      },
      
      // React specific
      react: {
        useSuspense: true,
        bindI18n: 'languageChanged loaded',
        bindI18nStore: 'added removed',
      },
    });
  
  return i18next;
}

export { i18next };
export default i18next;
```

### Types

```typescript
// apps/desktop/src/locales/types.ts

export interface SupportedLocale {
  code: string;
  name: string;
  nativeName: string;
  dir: 'ltr' | 'rtl';
}

// Type-safe translation keys
export type TranslationKey = 
  | `common.${keyof CommonTranslations}`
  | `ui.${keyof UITranslations}`
  | `capture.${keyof CaptureTranslations}`
  | `ai.${keyof AITranslations}`
  | `settings.${keyof SettingsTranslations}`
  | `marketplace.${keyof MarketplaceTranslations}`
  | `errors.${keyof ErrorTranslations}`;

// Example namespace types
export interface CommonTranslations {
  'app.name': string;
  'app.tagline': string;
  'actions.save': string;
  'actions.cancel': string;
  'actions.confirm': string;
  'actions.delete': string;
  'time.seconds': string; // ICU: {count, plural, ...}
  'time.minutes': string;
  'time.hours': string;
  'time.ago': string;
  'files.size': string;
  'files.count': string;
  // ... more
}

export interface UITranslations {
  'nav.home': string;
  'nav.clips': string;
  'nav.settings': string;
  'nav.marketplace': string;
  'header.recording': string;
  'header.stopped': string;
  'buttons.startRecording': string;
  'buttons.stopRecording': string;
  // ... more
}

// Extend for other namespaces...
export interface CaptureTranslations {}
export interface AITranslations {}
export interface SettingsTranslations {}
export interface MarketplaceTranslations {}
export interface ErrorTranslations {}
```

### Plugin Locale Loader

```typescript
// apps/desktop/src/locales/loader.ts

import i18next from 'i18next';
import type { Plugin } from '@clipshot/core';

/**
 * Loads plugin locales and merges with core translations.
 */
export class PluginLocaleLoader {
  private loadedPlugins: Set<string> = new Set();
  
  /**
   * Load locales for a plugin.
   */
  async loadPluginLocales(plugin: Plugin): Promise<void> {
    const { id, path } = plugin;
    
    if (this.loadedPlugins.has(id)) {
      return;
    }
    
    const currentLanguage = i18next.language;
    const fallbackLanguage = 'en';
    
    // Try to load current language
    let loaded = await this.tryLoadLocale(id, path, currentLanguage);
    
    // Fall back to language without region (tr-TR -> tr)
    if (!loaded && currentLanguage.includes('-')) {
      const baseLanguage = currentLanguage.split('-')[0];
      loaded = await this.tryLoadLocale(id, path, baseLanguage);
    }
    
    // Fall back to English
    if (!loaded) {
      await this.tryLoadLocale(id, path, fallbackLanguage);
    }
    
    this.loadedPlugins.add(id);
  }
  
  /**
   * Try to load a specific locale file.
   */
  private async tryLoadLocale(
    pluginId: string,
    pluginPath: string,
    language: string
  ): Promise<boolean> {
    try {
      const localePath = `${pluginPath}/locales/${language}.json`;
      const response = await fetch(localePath);
      
      if (!response.ok) {
        return false;
      }
      
      const translations = await response.json();
      
      // Add to plugin namespace
      i18next.addResourceBundle(
        language,
        `plugin:${pluginId}`,
        translations,
        true,  // deep merge
        true   // overwrite
      );
      
      console.log(`Loaded locale ${language} for plugin ${pluginId}`);
      return true;
      
    } catch (error) {
      console.warn(`Failed to load locale ${language} for plugin ${pluginId}`);
      return false;
    }
  }
  
  /**
   * Unload plugin locales.
   */
  unloadPluginLocales(pluginId: string): void {
    for (const language of SUPPORTED_LOCALES.map(l => l.code)) {
      i18next.removeResourceBundle(language, `plugin:${pluginId}`);
    }
    this.loadedPlugins.delete(pluginId);
  }
  
  /**
   * Get all loaded plugin namespaces.
   */
  getLoadedPluginNamespaces(): string[] {
    return Array.from(this.loadedPlugins).map(id => `plugin:${id}`);
  }
}

import { SUPPORTED_LOCALES } from './index';

// Singleton instance
export const pluginLocaleLoader = new PluginLocaleLoader();
```

---

## 🎨 REACT COMPONENTS

### Translation Hook

```typescript
// apps/desktop/src/hooks/useTypedTranslation.ts

import { useTranslation, UseTranslationOptions } from 'react-i18next';
import type { TranslationKey } from '../locales/types';

type Namespace = 
  | 'common' 
  | 'ui' 
  | 'capture' 
  | 'ai' 
  | 'settings' 
  | 'marketplace' 
  | 'errors'
  | `plugin:${string}`;

interface TypedTranslationOptions extends UseTranslationOptions<Namespace> {}

/**
 * Type-safe translation hook.
 */
export function useTypedTranslation(ns: Namespace = 'common') {
  const { t, i18n } = useTranslation(ns);
  
  return {
    t: (key: string, options?: Record<string, any>) => t(key, options),
    i18n,
    language: i18n.language,
    changeLanguage: i18n.changeLanguage,
  };
}

/**
 * Hook for accessing plugin translations.
 */
export function usePluginTranslation(pluginId: string) {
  return useTypedTranslation(`plugin:${pluginId}`);
}
```

### Language Selector Component

```tsx
// apps/desktop/src/components/LanguageSelector.tsx

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Globe, Check, ChevronDown } from 'lucide-react';
import { SUPPORTED_LOCALES, type SupportedLocale } from '../locales';

export const LanguageSelector: React.FC = () => {
  const { i18n } = useTranslation();
  const [open, setOpen] = useState(false);
  
  const currentLocale = SUPPORTED_LOCALES.find(
    l => l.code === i18n.language || i18n.language.startsWith(l.code)
  ) || SUPPORTED_LOCALES[0];
  
  const handleChange = async (locale: SupportedLocale) => {
    await i18n.changeLanguage(locale.code);
    
    // Update document direction for RTL languages
    document.documentElement.dir = locale.dir;
    document.documentElement.lang = locale.code;
    
    // Save preference
    localStorage.setItem('clipshot_language', locale.code);
    
    setOpen(false);
  };
  
  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-muted transition-colors"
      >
        <Globe className="w-4 h-4" />
        <span>{currentLocale.nativeName}</span>
        <ChevronDown className={`w-4 h-4 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>
      
      {open && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 z-40"
            onClick={() => setOpen(false)}
          />
          
          {/* Dropdown */}
          <div className="absolute right-0 mt-2 w-48 bg-popover border border-border rounded-lg shadow-lg z-50 max-h-80 overflow-auto">
            {SUPPORTED_LOCALES.map((locale) => (
              <button
                key={locale.code}
                onClick={() => handleChange(locale)}
                className="w-full flex items-center justify-between px-4 py-2 hover:bg-muted transition-colors"
              >
                <div className="flex flex-col items-start">
                  <span className="font-medium">{locale.nativeName}</span>
                  <span className="text-xs text-muted-foreground">{locale.name}</span>
                </div>
                {currentLocale.code === locale.code && (
                  <Check className="w-4 h-4 text-primary" />
                )}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
};
```

### Translated Text Component

```tsx
// apps/desktop/src/components/Trans.tsx

import React from 'react';
import { Trans as I18nTrans, TransProps } from 'react-i18next';

interface ClipShotTransProps extends Omit<TransProps<any>, 'i18nKey'> {
  i18nKey: string;
  values?: Record<string, any>;
  components?: Record<string, React.ReactElement>;
}

/**
 * Type-safe Trans component with common defaults.
 */
export const Trans: React.FC<ClipShotTransProps> = ({
  i18nKey,
  values,
  components,
  ...props
}) => {
  return (
    <I18nTrans
      i18nKey={i18nKey}
      values={values}
      components={{
        bold: <strong />,
        italic: <em />,
        code: <code className="bg-muted px-1 rounded" />,
        link: <a className="text-primary underline" />,
        ...components,
      }}
      {...props}
    />
  );
};

// Usage:
// <Trans
//   i18nKey="welcome.message"
//   values={{ name: 'John' }}
//   components={{ bold: <strong className="text-primary" /> }}
// />
//
// In locale file:
// "welcome.message": "Hello <bold>{name}</bold>! Welcome to ClipShot."
```

---

## 🔌 PLUGIN i18n API

### Plugin SDK

```typescript
// packages/plugin-sdk/src/i18n.ts

import type { Plugin } from './types';

export interface PluginI18nAPI {
  /**
   * Get translated string.
   */
  t(key: string, options?: Record<string, any>): string;
  
  /**
   * Get current language code.
   */
  getLanguage(): string;
  
  /**
   * Get all available languages for this plugin.
   */
  getAvailableLanguages(): string[];
  
  /**
   * Check if a translation key exists.
   */
  hasKey(key: string): boolean;
  
  /**
   * Listen for language changes.
   */
  onLanguageChange(callback: (language: string) => void): () => void;
}

/**
 * Create i18n API for a plugin.
 */
export function createPluginI18nAPI(pluginId: string): PluginI18nAPI {
  const namespace = `plugin:${pluginId}`;
  
  return {
    t(key, options) {
      return window.__clipshot_i18n__.t(`${namespace}:${key}`, options);
    },
    
    getLanguage() {
      return window.__clipshot_i18n__.language;
    },
    
    getAvailableLanguages() {
      return window.__clipshot_i18n__.getAvailableLanguages(namespace);
    },
    
    hasKey(key) {
      return window.__clipshot_i18n__.exists(`${namespace}:${key}`);
    },
    
    onLanguageChange(callback) {
      return window.__clipshot_i18n__.onLanguageChange(callback);
    },
  };
}
```

### Plugin Locale File Format

```json
// my-plugin/locales/en.json
{
  "$meta": {
    "language": "en",
    "plugin": "my-plugin",
    "version": "1.0.0",
    "authors": ["Author Name"]
  },
  
  "name": "My Plugin",
  "description": "A sample plugin for ClipShot",
  
  "settings": {
    "title": "My Plugin Settings",
    "option1": {
      "label": "Option 1",
      "description": "Description for option 1"
    },
    "option2": {
      "label": "Option 2",
      "description": "Description for option 2"
    }
  },
  
  "actions": {
    "process": "Process",
    "export": "Export to My Service"
  },
  
  "messages": {
    "success": "Operation completed successfully!",
    "error": "An error occurred: {message}",
    "progress": "Processing... {percent, number, ::percent}",
    "itemCount": "{count, plural, =0 {No items} one {# item} other {# items}}"
  },
  
  "ui": {
    "panel": {
      "title": "My Plugin Panel",
      "subtitle": "Manage your plugin settings"
    }
  }
}
```

```json
// my-plugin/locales/tr.json
{
  "$meta": {
    "language": "tr",
    "plugin": "my-plugin",
    "version": "1.0.0",
    "authors": ["Yazar Adı"]
  },
  
  "name": "Benim Eklentim",
  "description": "ClipShot için örnek bir eklenti",
  
  "settings": {
    "title": "Eklenti Ayarları",
    "option1": {
      "label": "Seçenek 1",
      "description": "Seçenek 1 için açıklama"
    },
    "option2": {
      "label": "Seçenek 2",
      "description": "Seçenek 2 için açıklama"
    }
  },
  
  "actions": {
    "process": "İşle",
    "export": "Servise Aktar"
  },
  
  "messages": {
    "success": "İşlem başarıyla tamamlandı!",
    "error": "Bir hata oluştu: {message}",
    "progress": "İşleniyor... {percent, number, ::percent}",
    "itemCount": "{count, plural, =0 {Öğe yok} one {# öğe} other {# öğe}}"
  },
  
  "ui": {
    "panel": {
      "title": "Eklenti Paneli",
      "subtitle": "Eklenti ayarlarınızı yönetin"
    }
  }
}
```

---

## 🔄 RTL SUPPORT

```css
/* apps/desktop/src/styles/rtl.css */

/* Base RTL support */
[dir="rtl"] {
  /* Flip horizontal margins and paddings */
  --space-start: var(--space-right);
  --space-end: var(--space-left);
}

/* Flip flex direction */
[dir="rtl"] .flex-row {
  flex-direction: row-reverse;
}

/* Flip text alignment */
[dir="rtl"] .text-left {
  text-align: right;
}

[dir="rtl"] .text-right {
  text-align: left;
}

/* Flip icons that have direction */
[dir="rtl"] .icon-arrow-right {
  transform: scaleX(-1);
}

[dir="rtl"] .icon-arrow-left {
  transform: scaleX(-1);
}

/* Sidebar position */
[dir="rtl"] .sidebar {
  left: auto;
  right: 0;
  border-left: 1px solid var(--border);
  border-right: none;
}

/* Scrollbar position */
[dir="rtl"] ::-webkit-scrollbar {
  left: 0;
  right: auto;
}

/* Progress bar direction */
[dir="rtl"] .progress-bar {
  direction: ltr; /* Keep progress left-to-right */
}
```

```typescript
// apps/desktop/src/hooks/useRTL.ts

import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { SUPPORTED_LOCALES } from '../locales';

/**
 * Hook to handle RTL layout changes.
 */
export function useRTL() {
  const { i18n } = useTranslation();
  
  useEffect(() => {
    const locale = SUPPORTED_LOCALES.find(
      l => l.code === i18n.language || i18n.language.startsWith(l.code)
    );
    
    if (locale) {
      document.documentElement.dir = locale.dir;
      document.documentElement.lang = locale.code;
      
      // Update body class for CSS targeting
      document.body.classList.remove('ltr', 'rtl');
      document.body.classList.add(locale.dir);
    }
  }, [i18n.language]);
  
  const isRTL = SUPPORTED_LOCALES.find(
    l => l.code === i18n.language || i18n.language.startsWith(l.code)
  )?.dir === 'rtl';
  
  return { isRTL };
}
```

---

## 📋 BACKEND i18n

```python
# src/core/i18n.py

import json
from pathlib import Path
from typing import Dict, Optional, Any
import babel
from babel.messages import frontend as babel_frontend
from babel.support import Translations

from src.core.logging import get_logger

logger = get_logger(__name__)


class I18nManager:
    """Backend internationalization manager."""
    
    LOCALE_DIR = Path(__file__).parent.parent / "locales"
    FALLBACK_LOCALE = "en"
    
    def __init__(self):
        self.translations: Dict[str, Translations] = {}
        self.current_locale = self.FALLBACK_LOCALE
    
    def load_locale(self, locale: str) -> bool:
        """Load translations for a locale."""
        locale_path = self.LOCALE_DIR / locale
        
        if not locale_path.exists():
            # Try without region (en-US -> en)
            if "-" in locale:
                base_locale = locale.split("-")[0]
                locale_path = self.LOCALE_DIR / base_locale
            
            if not locale_path.exists():
                logger.warning(f"Locale not found: {locale}")
                return False
        
        try:
            # Load .mo file if exists, otherwise load JSON
            mo_file = locale_path / "LC_MESSAGES" / "messages.mo"
            if mo_file.exists():
                self.translations[locale] = Translations.load(
                    str(locale_path), 
                    locales=[locale]
                )
            else:
                # Load JSON translations
                json_file = locale_path / "messages.json"
                if json_file.exists():
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    self.translations[locale] = JSONTranslations(data)
            
            logger.info(f"Loaded locale: {locale}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load locale {locale}: {e}")
            return False
    
    def set_locale(self, locale: str) -> bool:
        """Set the current locale."""
        if locale not in self.translations:
            if not self.load_locale(locale):
                return False
        
        self.current_locale = locale
        return True
    
    def translate(
        self, 
        key: str, 
        locale: Optional[str] = None,
        **kwargs
    ) -> str:
        """Translate a key."""
        locale = locale or self.current_locale
        
        translations = self.translations.get(locale)
        if not translations:
            translations = self.translations.get(self.FALLBACK_LOCALE)
        
        if not translations:
            return key
        
        result = translations.gettext(key)
        
        # Format with kwargs
        if kwargs:
            try:
                result = result.format(**kwargs)
            except KeyError:
                pass
        
        return result
    
    def ngettext(
        self, 
        singular: str, 
        plural: str, 
        n: int,
        **kwargs
    ) -> str:
        """Translate with pluralization."""
        locale = self.current_locale
        
        translations = self.translations.get(locale)
        if not translations:
            translations = self.translations.get(self.FALLBACK_LOCALE)
        
        if not translations:
            return singular if n == 1 else plural
        
        result = translations.ngettext(singular, plural, n)
        
        kwargs['n'] = n
        if kwargs:
            try:
                result = result.format(**kwargs)
            except KeyError:
                pass
        
        return result


class JSONTranslations:
    """Simple JSON-based translations."""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = self._flatten(data)
    
    def _flatten(
        self, 
        data: Dict[str, Any], 
        prefix: str = ""
    ) -> Dict[str, str]:
        """Flatten nested dict to dot notation."""
        result = {}
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                result.update(self._flatten(value, full_key))
            else:
                result[full_key] = str(value)
        return result
    
    def gettext(self, key: str) -> str:
        return self.data.get(key, key)
    
    def ngettext(self, singular: str, plural: str, n: int) -> str:
        # Simple pluralization
        return singular if n == 1 else plural


# Global instance
i18n = I18nManager()


# Helper functions
def _(key: str, **kwargs) -> str:
    """Translate a key."""
    return i18n.translate(key, **kwargs)


def _n(singular: str, plural: str, n: int, **kwargs) -> str:
    """Translate with pluralization."""
    return i18n.ngettext(singular, plural, n, **kwargs)
```

---

## 🎯 Bu Mimarinin Avantajları

1. **ICU Standard** — Profesyonel çoğullama ve format
2. **Type Safety** — TypeScript ile tip güvenliği
3. **Plugin Support** — Her plugin kendi çevirilerini getirir
4. **RTL Support** — Sağdan sola diller desteklenir
5. **Lazy Loading** — Sadece gerekli dil yüklenir
6. **Fallback Chain** — Eksik çeviriler için fallback
