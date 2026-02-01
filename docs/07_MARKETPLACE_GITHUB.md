# 🏪 MARKETPLACE & GITHUB — CLIPSHOT

> GitHub tabanlı plugin dağıtım sistemi, doğrulama, güven seviyeleri ve kurulum akışı.

---

## 🎯 MARKETPLACE PRENSİPLERİ

1. **Decentralized** — GitHub'da barındırılır, merkezi sunucu yok
2. **Open Source** — Tüm pluginler açık kaynak
3. **Validated** — Otomatik güvenlik ve kalite kontrolleri
4. **Trusted** — Güven seviyesi sistemi
5. **User Choice** — Kullanıcı kararı öncelikli

---

## 🏗️ MİMARİ

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIPSHOT APP                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    MARKETPLACE UI                          │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │  │
│  │  │ Featured │ │ Categories│ │ Search   │ │ Installed │     │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │  │
│  └────────────────────────┬──────────────────────────────────┘  │
│                           │                                      │
│  ┌────────────────────────▼──────────────────────────────────┐  │
│  │                 MARKETPLACE SERVICE                        │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │  │
│  │  │ GitHub API  │ │ Validator   │ │ Installer   │          │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘          │  │
│  └────────────────────────┬──────────────────────────────────┘  │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                         GITHUB                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              clipshot-plugins/registry                     │  │
│  │              (Central Plugin Registry)                     │  │
│  │  plugins.json                                              │  │
│  │  trust-levels.json                                         │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                │
│  │ author1/    │ │ author2/    │ │ author3/    │                │
│  │ plugin-a    │ │ plugin-b    │ │ plugin-c    │                │
│  │ manifest.json│ │ manifest.json│ │ manifest.json│             │
│  │ README.md   │ │ README.md   │ │ README.md   │                │
│  │ src/        │ │ src/        │ │ src/        │                │
│  └─────────────┘ └─────────────┘ └─────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 REGISTRY YAPISI

### Central Registry: `clipshot-plugins/registry`

```json
// plugins.json
{
  "$schema": "https://clipshot.dev/schemas/registry.json",
  "version": "1.0.0",
  "plugins": [
    {
      "id": "official.obs-capture",
      "repo": "clipshot-plugins/obs-capture",
      "name": "OBS Capture",
      "description": "Record clips using OBS Studio",
      "category": "capture",
      "trust_level": "official",
      "featured": true,
      "downloads": 15420,
      "rating": 4.8,
      "tags": ["obs", "capture", "recording"],
      "latest_version": "1.2.0",
      "min_clipshot_version": "1.0.0"
    },
    {
      "id": "community.discord-share",
      "repo": "username/clipshot-discord-share",
      "name": "Discord Share",
      "description": "Share clips directly to Discord",
      "category": "export",
      "trust_level": "verified",
      "featured": false,
      "downloads": 8234,
      "rating": 4.5,
      "tags": ["discord", "share", "social"],
      "latest_version": "2.0.1",
      "min_clipshot_version": "1.0.0"
    }
  ],
  "categories": [
    { "id": "capture", "name": "Capture", "icon": "video" },
    { "id": "ai", "name": "AI", "icon": "brain" },
    { "id": "export", "name": "Export", "icon": "upload" },
    { "id": "editor", "name": "Editor", "icon": "scissors" },
    { "id": "theme", "name": "Themes", "icon": "palette" },
    { "id": "utility", "name": "Utilities", "icon": "tool" }
  ],
  "updated_at": "2024-01-15T12:00:00Z"
}
```

### Trust Levels: `trust-levels.json`

```json
// trust-levels.json
{
  "levels": {
    "official": {
      "label": "Official",
      "badge": "🔷",
      "color": "#0066ff",
      "description": "Maintained by ClipShot team",
      "auto_approve": true,
      "permissions_review": false
    },
    "verified": {
      "label": "Verified",
      "badge": "✅",
      "color": "#00cc66",
      "description": "Code reviewed by community",
      "auto_approve": true,
      "permissions_review": true
    },
    "community": {
      "label": "Community",
      "badge": "👥",
      "color": "#9966ff",
      "description": "Community contributed",
      "auto_approve": false,
      "permissions_review": true
    },
    "unverified": {
      "label": "Unverified",
      "badge": "⚠️",
      "color": "#ffcc00",
      "description": "Not yet reviewed",
      "auto_approve": false,
      "permissions_review": true,
      "warning": true
    }
  },
  "verified_developers": [
    { "github": "clipshot-official", "level": "official" },
    { "github": "trusted-dev-1", "level": "verified" },
    { "github": "trusted-dev-2", "level": "verified" }
  ]
}
```

---

## 🔧 PLUGIN REPOSITORY YAPISI

### Minimum Gereksinimler

```
my-plugin/
├── manifest.json       # REQUIRED: Plugin metadata
├── README.md           # REQUIRED: User documentation
├── LICENSE             # REQUIRED: Open source license
├── CHANGELOG.md        # RECOMMENDED: Version history
├── src/                # Plugin source code
│   ├── main.ts         # Main entry point
│   └── ...
├── locales/            # Translations
│   ├── en.json
│   └── tr.json
├── assets/             # Icons and images
│   ├── icon.png        # 256x256 plugin icon
│   └── screenshots/
│       ├── 1.png
│       └── 2.png
└── .clipshot/          # ClipShot specific files
    └── validation.json # Auto-generated validation results
```

### manifest.json Gereksinimleri

```json
{
  "id": "author.plugin-name",
  "name": "Plugin Name",
  "version": "1.0.0",
  "description": "Brief description",
  "author": {
    "name": "Author Name",
    "github": "github-username",
    "email": "author@example.com"
  },
  "license": "MIT",
  "repository": "https://github.com/author/plugin-name",
  "homepage": "https://plugin-website.com",
  "bugs": "https://github.com/author/plugin-name/issues",
  
  "clipshot": ">=1.0.0",
  "main": "./dist/main.js",
  "category": "utility",
  
  "permissions": {
    "required": ["filesystem"],
    "optional": ["network"]
  },
  
  "provides": [],
  "requires": [],
  "conflicts": []
}
```

---

## 🔄 KURULUM AKIŞI

```python
# src/marketplace/installer.py

import asyncio
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
import aiohttp
import zipfile
import json

from src.core.logging import get_logger
from src.plugins.validator import PluginValidator
from src.plugins.conflict import ConflictDetector
from src.marketplace.trust import TrustManager

logger = get_logger(__name__)


class PluginInstaller:
    """Handles plugin installation from GitHub."""
    
    def __init__(self):
        self.plugins_dir = Path.home() / ".clipshot" / "plugins"
        self.temp_dir = Path.home() / ".clipshot" / "temp"
        self.validator = PluginValidator()
        self.conflict_detector = ConflictDetector()
        self.trust_manager = TrustManager()
    
    async def install_from_github(
        self,
        repo: str,  # "owner/repo"
        version: Optional[str] = None,
        force: bool = False,
    ) -> Dict[str, Any]:
        """Install a plugin from GitHub repository."""
        result = {
            "success": False,
            "plugin_id": None,
            "version": None,
            "errors": [],
            "warnings": [],
        }
        
        try:
            # Step 1: Fetch release info
            release = await self._fetch_release(repo, version)
            if not release:
                result["errors"].append(f"Release not found for {repo}")
                return result
            
            # Step 2: Download and extract
            temp_path = await self._download_release(release)
            if not temp_path:
                result["errors"].append("Failed to download release")
                return result
            
            # Step 3: Load and validate manifest
            manifest = await self._load_manifest(temp_path)
            if not manifest:
                result["errors"].append("Invalid or missing manifest.json")
                return result
            
            # Step 4: Security validation
            validation = await self.validator.validate(temp_path, manifest)
            if not validation["passed"]:
                result["errors"].extend(validation["errors"])
                return result
            result["warnings"].extend(validation["warnings"])
            
            # Step 5: Check trust level
            trust_level = await self.trust_manager.get_trust_level(
                repo, 
                manifest["author"]["github"]
            )
            if trust_level == "unverified":
                result["warnings"].append("This plugin is unverified. Install at your own risk.")
            
            # Step 6: Check conflicts
            conflicts = self.conflict_detector.check_conflicts(manifest)
            for conflict in conflicts:
                if conflict.severity.value == "error":
                    result["errors"].append(conflict.message)
                else:
                    result["warnings"].append(conflict.message)
            
            if result["errors"]:
                return result
            
            # Step 7: Check if already installed
            plugin_id = manifest["id"]
            install_path = self.plugins_dir / plugin_id
            
            if install_path.exists() and not force:
                result["errors"].append(f"Plugin {plugin_id} is already installed. Use force=True to reinstall.")
                return result
            
            # Step 8: Install
            if install_path.exists():
                shutil.rmtree(install_path)
            
            shutil.copytree(temp_path, install_path)
            
            # Step 9: Register plugin
            self.conflict_detector.register_plugin(plugin_id, manifest)
            
            result["success"] = True
            result["plugin_id"] = plugin_id
            result["version"] = manifest["version"]
            result["trust_level"] = trust_level
            
            logger.info(f"Successfully installed plugin: {plugin_id} v{manifest['version']}")
            
        except Exception as e:
            logger.error(f"Plugin installation failed: {e}")
            result["errors"].append(str(e))
        
        finally:
            # Cleanup temp
            if "temp_path" in locals() and temp_path.exists():
                shutil.rmtree(temp_path, ignore_errors=True)
        
        return result
    
    async def _fetch_release(
        self, 
        repo: str, 
        version: Optional[str]
    ) -> Optional[dict]:
        """Fetch release information from GitHub."""
        async with aiohttp.ClientSession() as session:
            if version:
                url = f"https://api.github.com/repos/{repo}/releases/tags/v{version}"
            else:
                url = f"https://api.github.com/repos/{repo}/releases/latest"
            
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                return None
    
    async def _download_release(self, release: dict) -> Optional[Path]:
        """Download and extract release."""
        # Find the source zip
        zipball_url = release.get("zipball_url")
        if not zipball_url:
            return None
        
        temp_path = self.temp_dir / f"download_{release['id']}"
        temp_path.mkdir(parents=True, exist_ok=True)
        
        zip_path = temp_path / "source.zip"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(zipball_url) as response:
                if response.status != 200:
                    return None
                
                content = await response.read()
                with open(zip_path, "wb") as f:
                    f.write(content)
        
        # Extract
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(temp_path)
        
        # Find extracted folder (GitHub adds prefix)
        extracted = [d for d in temp_path.iterdir() if d.is_dir()]
        if extracted:
            return extracted[0]
        
        return None
    
    async def _load_manifest(self, path: Path) -> Optional[dict]:
        """Load and parse manifest.json."""
        manifest_path = path / "manifest.json"
        if not manifest_path.exists():
            return None
        
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None
    
    async def uninstall(self, plugin_id: str) -> bool:
        """Uninstall a plugin."""
        install_path = self.plugins_dir / plugin_id
        
        if not install_path.exists():
            logger.warning(f"Plugin not found: {plugin_id}")
            return False
        
        try:
            shutil.rmtree(install_path)
            self.conflict_detector.unregister_plugin(plugin_id)
            logger.info(f"Uninstalled plugin: {plugin_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to uninstall plugin {plugin_id}: {e}")
            return False
    
    async def update(
        self, 
        plugin_id: str, 
        version: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update a plugin to a new version."""
        install_path = self.plugins_dir / plugin_id
        
        if not install_path.exists():
            return {"success": False, "errors": ["Plugin not installed"]}
        
        # Get current manifest
        manifest_path = install_path / "manifest.json"
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
        
        repo = manifest.get("repository", "").replace("https://github.com/", "")
        
        return await self.install_from_github(repo, version, force=True)
```

---

## 🔒 SECURITY VALIDATION

```python
# src/plugins/validator.py

import ast
import re
from pathlib import Path
from typing import Dict, Any, List
import json

from src.core.logging import get_logger

logger = get_logger(__name__)


class PluginValidator:
    """Validates plugin security and compliance."""
    
    # Dangerous patterns to detect
    DANGEROUS_PATTERNS = [
        # OS command execution
        (r"subprocess\.(call|run|Popen)", "Process execution detected"),
        (r"os\.system\s*\(", "OS command execution detected"),
        (r"os\.popen\s*\(", "OS command execution detected"),
        (r"eval\s*\(", "eval() is not allowed"),
        (r"exec\s*\(", "exec() is not allowed"),
        (r"__import__\s*\(", "Dynamic import detected"),
        
        # File system access outside sandbox
        (r"open\s*\(\s*['\"][\/\\]", "Absolute path access detected"),
        (r"Path\s*\(\s*['\"][\/\\]", "Absolute path access detected"),
        
        # Network without permission
        (r"socket\.socket", "Direct socket usage detected"),
        (r"urllib", "Direct network access detected"),
        (r"requests\.", "Direct network access detected"),
        
        # Windows specific
        (r"ctypes\.windll", "Windows API access detected"),
        (r"win32api", "Windows API access detected"),
        
        # Crypto mining indicators
        (r"stratum\+tcp", "Possible crypto mining detected"),
        (r"hashrate", "Possible crypto mining detected"),
    ]
    
    # Required manifest fields
    REQUIRED_MANIFEST_FIELDS = [
        "id", "name", "version", "description", "author", "license",
        "clipshot", "main", "permissions"
    ]
    
    async def validate(
        self, 
        plugin_path: Path, 
        manifest: dict
    ) -> Dict[str, Any]:
        """Validate a plugin for security and compliance."""
        result = {
            "passed": True,
            "errors": [],
            "warnings": [],
            "security_score": 100,
        }
        
        # 1. Validate manifest
        manifest_result = self._validate_manifest(manifest)
        result["errors"].extend(manifest_result["errors"])
        result["warnings"].extend(manifest_result["warnings"])
        
        # 2. Scan source code
        code_result = await self._scan_source_code(plugin_path)
        result["errors"].extend(code_result["errors"])
        result["warnings"].extend(code_result["warnings"])
        result["security_score"] -= code_result["deductions"]
        
        # 3. Check file structure
        structure_result = self._validate_structure(plugin_path)
        result["errors"].extend(structure_result["errors"])
        result["warnings"].extend(structure_result["warnings"])
        
        # 4. Validate permissions
        permissions_result = self._validate_permissions(manifest)
        result["warnings"].extend(permissions_result["warnings"])
        
        # Set final status
        result["passed"] = len(result["errors"]) == 0
        result["security_score"] = max(0, result["security_score"])
        
        return result
    
    def _validate_manifest(self, manifest: dict) -> Dict[str, Any]:
        """Validate manifest structure and content."""
        errors = []
        warnings = []
        
        # Check required fields
        for field in self.REQUIRED_MANIFEST_FIELDS:
            if field not in manifest:
                errors.append(f"Missing required manifest field: {field}")
        
        # Validate ID format
        if "id" in manifest:
            if not re.match(r"^[\w-]+\.[\w-]+$", manifest["id"]):
                errors.append("Invalid plugin ID format. Use 'author.plugin-name'")
        
        # Validate version format
        if "version" in manifest:
            if not re.match(r"^\d+\.\d+\.\d+", manifest["version"]):
                warnings.append("Version should follow semver (x.y.z)")
        
        # Validate author
        if "author" in manifest:
            if not isinstance(manifest["author"], dict):
                errors.append("Author must be an object with name, github, email")
            elif "github" not in manifest["author"]:
                warnings.append("Author github username recommended")
        
        # Validate license
        if "license" in manifest:
            valid_licenses = ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "ISC"]
            if manifest["license"] not in valid_licenses:
                warnings.append(f"Consider using a standard license: {valid_licenses}")
        
        return {"errors": errors, "warnings": warnings}
    
    async def _scan_source_code(
        self, 
        plugin_path: Path
    ) -> Dict[str, Any]:
        """Scan source code for dangerous patterns."""
        errors = []
        warnings = []
        deductions = 0
        
        # Scan all Python and JavaScript/TypeScript files
        extensions = ["*.py", "*.js", "*.ts", "*.tsx", "*.jsx"]
        
        for ext in extensions:
            for file_path in plugin_path.rglob(ext):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    for pattern, message in self.DANGEROUS_PATTERNS:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            relative_path = file_path.relative_to(plugin_path)
                            errors.append(f"{message} in {relative_path}")
                            deductions += 20
                            
                except Exception as e:
                    warnings.append(f"Could not scan {file_path.name}: {e}")
        
        return {"errors": errors, "warnings": warnings, "deductions": deductions}
    
    def _validate_structure(self, plugin_path: Path) -> Dict[str, Any]:
        """Validate plugin file structure."""
        errors = []
        warnings = []
        
        required_files = ["manifest.json", "README.md"]
        recommended_files = ["LICENSE", "CHANGELOG.md"]
        
        for file in required_files:
            if not (plugin_path / file).exists():
                errors.append(f"Missing required file: {file}")
        
        for file in recommended_files:
            if not (plugin_path / file).exists():
                warnings.append(f"Missing recommended file: {file}")
        
        # Check for suspicious files
        suspicious_extensions = [".exe", ".dll", ".so", ".dylib", ".bat", ".sh", ".ps1"]
        for ext in suspicious_extensions:
            for file in plugin_path.rglob(f"*{ext}"):
                errors.append(f"Binary/executable file not allowed: {file.name}")
        
        return {"errors": errors, "warnings": warnings}
    
    def _validate_permissions(self, manifest: dict) -> Dict[str, Any]:
        """Validate permission declarations."""
        warnings = []
        
        permissions = manifest.get("permissions", {})
        required = permissions.get("required", [])
        optional = permissions.get("optional", [])
        
        # Warn about high-risk permissions
        high_risk = ["system", "network", "filesystem"]
        
        for perm in required:
            if perm in high_risk:
                warnings.append(f"Plugin requires high-risk permission: {perm}")
        
        # Check for reasonable permissions
        all_perms = required + optional
        if not all_perms:
            warnings.append("Plugin declares no permissions - consider if any are needed")
        
        return {"warnings": warnings}
```

---

## 📋 API ENDPOINTS

```python
# src/api/routers/marketplace.py

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import Optional, List
from pydantic import BaseModel

from src.marketplace.installer import PluginInstaller
from src.marketplace.search import MarketplaceSearch

router = APIRouter(prefix="/marketplace", tags=["marketplace"])
installer = PluginInstaller()
search = MarketplaceSearch()


class InstallRequest(BaseModel):
    repo: str
    version: Optional[str] = None
    force: bool = False


class SearchQuery(BaseModel):
    query: str
    category: Optional[str] = None
    trust_level: Optional[str] = None
    page: int = 1
    per_page: int = 20


@router.get("/plugins")
async def list_plugins(
    category: Optional[str] = None,
    featured: bool = False,
    sort_by: str = Query("downloads", enum=["downloads", "rating", "updated"]),
    page: int = 1,
    per_page: int = 20,
):
    """List available plugins from registry."""
    return await search.list_plugins(
        category=category,
        featured=featured,
        sort_by=sort_by,
        page=page,
        per_page=per_page,
    )


@router.post("/search")
async def search_plugins(query: SearchQuery):
    """Search for plugins."""
    return await search.search(
        query=query.query,
        category=query.category,
        trust_level=query.trust_level,
        page=query.page,
        per_page=query.per_page,
    )


@router.get("/plugins/{plugin_id}")
async def get_plugin_details(plugin_id: str):
    """Get detailed information about a plugin."""
    details = await search.get_plugin_details(plugin_id)
    if not details:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return details


@router.post("/install")
async def install_plugin(request: InstallRequest, background: BackgroundTasks):
    """Install a plugin from GitHub."""
    result = await installer.install_from_github(
        repo=request.repo,
        version=request.version,
        force=request.force,
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=400, 
            detail={"errors": result["errors"], "warnings": result["warnings"]}
        )
    
    return result


@router.delete("/plugins/{plugin_id}")
async def uninstall_plugin(plugin_id: str):
    """Uninstall a plugin."""
    success = await installer.uninstall(plugin_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return {"success": True, "plugin_id": plugin_id}


@router.post("/plugins/{plugin_id}/update")
async def update_plugin(plugin_id: str, version: Optional[str] = None):
    """Update a plugin to a new version."""
    result = await installer.update(plugin_id, version)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["errors"])
    
    return result


@router.get("/categories")
async def list_categories():
    """List available plugin categories."""
    return await search.get_categories()


@router.get("/installed")
async def list_installed():
    """List installed plugins."""
    from src.plugins.manager import PluginManager
    manager = PluginManager()
    return await manager.list_installed()
```

---

## 🌐 FRONTEND COMPONENTS

```typescript
// apps/desktop/src/renderer/pages/Marketplace.tsx

import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Search, Download, Star, Shield, Package } from 'lucide-react';

interface Plugin {
  id: string;
  name: string;
  description: string;
  author: string;
  version: string;
  downloads: number;
  rating: number;
  trust_level: 'official' | 'verified' | 'community' | 'unverified';
  category: string;
  installed: boolean;
}

const trustBadges = {
  official: { icon: '🔷', label: 'Official', color: 'text-blue-500' },
  verified: { icon: '✅', label: 'Verified', color: 'text-green-500' },
  community: { icon: '👥', label: 'Community', color: 'text-purple-500' },
  unverified: { icon: '⚠️', label: 'Unverified', color: 'text-yellow-500' },
};

export const Marketplace: React.FC = () => {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState<string | null>(null);
  const [installing, setInstalling] = useState<string | null>(null);

  // Fetch plugins
  const { data: plugins, isLoading, refetch } = useQuery({
    queryKey: ['marketplace', 'plugins', search, category],
    queryFn: () => window.clipshot.marketplace.search({ query: search, category }),
  });

  // Fetch categories
  const { data: categories } = useQuery({
    queryKey: ['marketplace', 'categories'],
    queryFn: () => window.clipshot.marketplace.getCategories(),
  });

  // Install mutation
  const installMutation = useMutation({
    mutationFn: (plugin: Plugin) => 
      window.clipshot.marketplace.install({ repo: plugin.id }),
    onSuccess: () => refetch(),
  });

  const handleInstall = async (plugin: Plugin) => {
    if (plugin.trust_level === 'unverified') {
      const confirmed = await window.clipshot.dialog.confirm({
        title: 'Install Unverified Plugin?',
        message: `"${plugin.name}" is not verified. Install at your own risk.`,
        type: 'warning',
      });
      if (!confirmed) return;
    }

    setInstalling(plugin.id);
    await installMutation.mutateAsync(plugin);
    setInstalling(null);
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-border">
        <h1 className="text-2xl font-bold mb-4">Plugin Marketplace</h1>
        
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search plugins..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-lg bg-muted"
          />
        </div>
        
        {/* Categories */}
        <div className="flex gap-2 mt-4 flex-wrap">
          <button
            onClick={() => setCategory(null)}
            className={`px-3 py-1 rounded-full text-sm ${
              !category ? 'bg-primary text-primary-foreground' : 'bg-muted'
            }`}
          >
            All
          </button>
          {categories?.map((cat: any) => (
            <button
              key={cat.id}
              onClick={() => setCategory(cat.id)}
              className={`px-3 py-1 rounded-full text-sm ${
                category === cat.id ? 'bg-primary text-primary-foreground' : 'bg-muted'
              }`}
            >
              {cat.name}
            </button>
          ))}
        </div>
      </div>

      {/* Plugin Grid */}
      <div className="flex-1 overflow-auto p-6">
        {isLoading ? (
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {plugins?.items.map((plugin: Plugin) => (
              <PluginCard
                key={plugin.id}
                plugin={plugin}
                installing={installing === plugin.id}
                onInstall={() => handleInstall(plugin)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

interface PluginCardProps {
  plugin: Plugin;
  installing: boolean;
  onInstall: () => void;
}

const PluginCard: React.FC<PluginCardProps> = ({ plugin, installing, onInstall }) => {
  const badge = trustBadges[plugin.trust_level];

  return (
    <div className="bg-card rounded-lg border border-border p-4 hover:border-primary/50 transition-colors">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-lg bg-muted flex items-center justify-center">
            <Package className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-medium">{plugin.name}</h3>
            <p className="text-sm text-muted-foreground">{plugin.author}</p>
          </div>
        </div>
        <span className={`text-lg ${badge.color}`} title={badge.label}>
          {badge.icon}
        </span>
      </div>

      {/* Description */}
      <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
        {plugin.description}
      </p>

      {/* Stats */}
      <div className="flex items-center gap-4 text-sm text-muted-foreground mb-4">
        <span className="flex items-center gap-1">
          <Download className="w-4 h-4" />
          {plugin.downloads.toLocaleString()}
        </span>
        <span className="flex items-center gap-1">
          <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
          {plugin.rating.toFixed(1)}
        </span>
        <span>v{plugin.version}</span>
      </div>

      {/* Action */}
      <button
        onClick={onInstall}
        disabled={plugin.installed || installing}
        className={`w-full py-2 rounded-lg font-medium transition-colors ${
          plugin.installed
            ? 'bg-muted text-muted-foreground cursor-not-allowed'
            : 'bg-primary text-primary-foreground hover:bg-primary/90'
        }`}
      >
        {installing ? (
          <span className="flex items-center justify-center gap-2">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current" />
            Installing...
          </span>
        ) : plugin.installed ? (
          'Installed'
        ) : (
          'Install'
        )}
      </button>
    </div>
  );
};
```

---

## 🎯 Bu Mimarinin Avantajları

1. **Decentralized** — Merkezi sunucu bağımlılığı yok
2. **Transparent** — Tüm kod GitHub'da görünür
3. **Validated** — Otomatik güvenlik taraması
4. **User Control** — Kullanıcı son kararı verir
5. **Extensible** — Kolayca yeni pluginler eklenebilir
6. **Trust Levels** — Güvenilirlik seviyesi gösterilir
