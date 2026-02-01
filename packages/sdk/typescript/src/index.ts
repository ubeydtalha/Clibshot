/**
 * ClipShot Plugin SDK for TypeScript
 * 
 * This SDK provides the types and interfaces for developing ClipShot plugins
 * in TypeScript/JavaScript.
 */

/**
 * Plugin metadata information
 */
export interface PluginInfo {
  id: string;
  name: string;
  version: string;
  author: string;
  description: string;
}

/**
 * Represents a captured clip
 */
export interface Clip {
  id: string;
  title: string;
  game?: string;
  duration: number;
  width: number;
  height: number;
  fps: number;
  filePath: string;
  metadata: Record<string, any>;
  createdAt: Date;
}

/**
 * Represents a detected game
 */
export interface Game {
  id: string;
  name: string;
  processName: string;
  windowTitle: string;
  detectedAt: Date;
}

/**
 * Plugin configuration type
 */
export type PluginConfig = Record<string, any>;

/**
 * Plugin context provided during initialization
 */
export interface PluginContext {
  /**
   * Get plugin configuration
   */
  getConfig(): Promise<PluginConfig>;
  
  /**
   * Get a logger instance for the plugin
   */
  getLogger(): Logger;
  
  /**
   * Get a core API instance
   */
  getApi<T>(apiClass: new () => T): Promise<T>;
}

/**
 * Logger interface
 */
export interface Logger {
  info(message: string, ...args: any[]): void;
  warn(message: string, ...args: any[]): void;
  error(message: string, ...args: any[]): void;
  debug(message: string, ...args: any[]): void;
}

/**
 * Base Plugin interface
 * 
 * All ClipShot plugins must implement this interface.
 * 
 * @example
 * ```typescript
 * export class MyPlugin implements ClipShotPlugin {
 *   id = "com.example.my-plugin";
 *   name = "My Plugin";
 *   version = "1.0.0";
 *   
 *   async init(context: PluginContext): Promise<void> {
 *     const config = await context.getConfig();
 *     const logger = context.getLogger();
 *     logger.info("Plugin initialized!");
 *   }
 *   
 *   async shutdown(): Promise<void> {
 *     // Cleanup
 *   }
 *   
 *   async onClipCaptured(clip: Clip): Promise<void> {
 *     console.log("Clip captured:", clip.id);
 *   }
 * }
 * ```
 */
export interface ClipShotPlugin {
  /**
   * Unique plugin identifier (reverse domain notation)
   */
  id: string;
  
  /**
   * Display name of the plugin
   */
  name: string;
  
  /**
   * Plugin version (semantic versioning)
   */
  version: string;
  
  /**
   * Initialize the plugin
   * 
   * @param context - Plugin context with configuration and APIs
   */
  init(context: PluginContext): Promise<void>;
  
  /**
   * Shutdown the plugin
   * 
   * Called when the plugin is being unloaded.
   */
  shutdown(): Promise<void>;
  
  /**
   * Called when a clip is captured
   * 
   * @param clip - The captured clip
   */
  onClipCaptured?(clip: Clip): Promise<void>;
  
  /**
   * Called when a game is detected
   * 
   * @param game - The detected game
   */
  onGameDetected?(game: Game): Promise<void>;
  
  /**
   * Called when plugin configuration changes
   * 
   * @param newConfig - The new configuration
   */
  onConfigChanged?(newConfig: PluginConfig): Promise<void>;
}

/**
 * API route metadata
 */
export interface ApiRouteMetadata {
  path: string;
  methods: string[];
}

/**
 * Decorator for registering custom API routes
 * 
 * @example
 * ```typescript
 * class MyPlugin implements ClipShotPlugin {
 *   @apiRoute("/status", ["GET"])
 *   async getStatus(): Promise<{ status: string }> {
 *     return { status: "healthy" };
 *   }
 * }
 * ```
 */
export function apiRoute(path: string, methods: string[] = ["GET"]) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const metadata: ApiRouteMetadata = { path, methods };
    Reflect.defineMetadata("api:route", metadata, target, propertyKey);
    return descriptor;
  };
}

/**
 * Event types
 */
export enum EventType {
  ClipCaptured = "clip.captured",
  GameDetected = "game.detected",
  ConfigChanged = "config.changed",
}

/**
 * Base event interface
 */
export interface Event<T = any> {
  type: EventType;
  data: T;
  timestamp: Date;
}

/**
 * Core API types
 */
export interface CaptureAPI {
  startCapture(gameId: string): Promise<void>;
  stopCapture(): Promise<void>;
  isCapturing(): Promise<boolean>;
}

export interface ClipAPI {
  getClip(id: string): Promise<Clip>;
  listClips(filters?: Record<string, any>): Promise<Clip[]>;
  deleteClip(id: string): Promise<void>;
}

export interface MetadataAPI {
  generate(clipId: string): Promise<Record<string, any>>;
  update(clipId: string, metadata: Record<string, any>): Promise<void>;
}

export interface EventBus {
  subscribe(eventType: EventType, handler: (event: Event) => void): void;
  unsubscribe(eventType: EventType, handler: (event: Event) => void): void;
  emit(event: Event): void;
}

/**
 * Plugin manifest schema
 */
export interface PluginManifest {
  id: string;
  name: string;
  version: string;
  api_version: string;
  type: "core" | "optional" | "ai" | "ui" | "system";
  category: "capture" | "ai" | "editor" | "social" | "enhancement" | "codec" | "template" | "analytics";
  description: Record<string, string>;
  author: {
    name: string;
    email: string;
    url?: string;
  };
  repository?: string;
  license: string;
  homepage?: string;
  bugs?: string;
  keywords?: string[];
  entry: {
    backend?: string;
    frontend?: string;
  };
  permissions?: Record<string, any>;
  capabilities?: string[];
  provides?: string[];
  requires?: string[];
  conflicts?: string[];
  settings?: {
    schema: string;
    defaults: Record<string, any>;
  };
  ui?: {
    settingsPanel?: boolean;
    toolbar?: boolean;
    sidebar?: boolean;
    overlay?: boolean;
  };
  localization?: {
    supported: string[];
    fallback: string;
    path: string;
  };
  resources?: {
    cpu?: { max_percent: number };
    memory?: { max_mb: number };
    gpu?: { max_percent: number };
  };
  platforms?: string[];
  engines?: {
    clipshot?: string;
    python?: string;
    node?: string;
  };
}

/**
 * Export all types
 */
export * from "./types";
