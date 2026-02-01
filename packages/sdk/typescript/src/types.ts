/**
 * Additional type definitions for ClipShot SDK
 */

/**
 * Permission levels
 */
export type PermissionLevel = "none" | "limited" | "optional" | "required";

/**
 * Permission entry
 */
export interface PermissionEntry {
  level: PermissionLevel;
  reason?: Record<string, string>;
}

/**
 * Filesystem permission
 */
export interface FilesystemPermission extends PermissionEntry {
  paths?: string[];
  operations?: ("read" | "write")[];
}

/**
 * Network permission
 */
export interface NetworkPermission extends PermissionEntry {
  hosts?: string[];
  protocols?: string[];
}

/**
 * System permission
 */
export interface SystemPermission extends PermissionEntry {
  apis?: string[];
}

/**
 * Complete permissions object
 */
export interface Permissions {
  screen?: PermissionEntry;
  microphone?: PermissionEntry;
  filesystem?: FilesystemPermission;
  network?: NetworkPermission;
  gpu?: PermissionEntry;
  system?: SystemPermission;
  clipboard?: PermissionEntry;
  notifications?: PermissionEntry;
}
