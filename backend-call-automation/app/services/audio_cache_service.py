"""
Servicio para gestionar el caché de audio generado.

Este módulo proporciona funcionalidades para almacenar y recuperar
archivos de audio generados, optimizando el rendimiento y reduciendo
las llamadas a servicios externos de generación de voz.
"""

import hashlib
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

from fastapi import UploadFile
from app.config.redis_client import get_from_cache, set_in_cache, delete_from_cache
from app.config.settings import get_settings
from app.utils.logging import app_logger

logger = app_logger

# Configuración
settings = get_settings()
AUDIO_CACHE_DIR = settings.AUDIO_CACHE_DIR
AUDIO_CACHE_TTL = settings.AUDIO_CACHE_TTL
AUDIO_CACHE_MAX_SIZE = settings.AUDIO_CACHE_MAX_SIZE
AUDIO_CACHE_ENABLED = settings.AUDIO_CACHE_ENABLED

# Crear directorio de caché si no existe
os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)


class AudioCacheService:
    """
    Servicio para gestionar el caché de audio generado.
    
    Este servicio proporciona métodos para almacenar y recuperar
    archivos de audio generados, optimizando el rendimiento y reduciendo
    las llamadas a servicios externos de generación de voz.
    """
    
    def __init__(self):
        """
        Inicializa el servicio de caché de audio.
        """
        self.cache_dir = AUDIO_CACHE_DIR
        self.cache_ttl = AUDIO_CACHE_TTL
        self.max_cache_size = AUDIO_CACHE_MAX_SIZE
        self.enabled = AUDIO_CACHE_ENABLED
        self.metadata_key = "audio_cache_metadata"
        
        # Inicializar metadata si no existe
        self._init_metadata()
    
    def _init_metadata(self):
        """
        Inicializa los metadatos del caché si no existen.
        """
        if not os.path.exists(os.path.join(self.cache_dir, "metadata.json")):
            metadata = {
                "files": {},
                "total_size": 0,
                "last_cleanup": datetime.now().isoformat(),
            }
            self._save_metadata(metadata)
    
    def _save_metadata(self, metadata: Dict[str, Any]):
        """
        Guarda los metadatos del caché en un archivo JSON.
        
        Args:
            metadata: Diccionario con los metadatos a guardar
        """
        try:
            with open(os.path.join(self.cache_dir, "metadata.json"), "w") as f:
                json.dump(metadata, f)
        except Exception as e:
            logger.error(f"Error al guardar metadatos de caché de audio: {str(e)}")
    
    def _load_metadata(self) -> Dict[str, Any]:
        """
        Carga los metadatos del caché desde un archivo JSON.
        
        Returns:
            Diccionario con los metadatos del caché
        """
        try:
            with open(os.path.join(self.cache_dir, "metadata.json"), "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error al cargar metadatos de caché de audio: {str(e)}")
            return {"files": {}, "total_size": 0, "last_cleanup": datetime.now().isoformat()}
    
    def _generate_cache_key(self, text: str, voice_id: str, language: str = "es") -> str:
        """
        Genera una clave única para el caché basada en el texto y la voz.
        
        Args:
            text: Texto a convertir en audio
            voice_id: ID de la voz a utilizar
            language: Idioma del texto
            
        Returns:
            Clave única para el caché
        """
        # Normalizar texto (eliminar espacios extra, convertir a minúsculas)
        normalized_text = " ".join(text.lower().split())
        
        # Crear hash del texto + voz + idioma
        hash_input = f"{normalized_text}|{voice_id}|{language}"
        hash_value = hashlib.md5(hash_input.encode()).hexdigest()
        
        return hash_value
    
    def _get_file_path(self, cache_key: str) -> str:
        """
        Obtiene la ruta del archivo de audio en el caché.
        
        Args:
            cache_key: Clave única del caché
            
        Returns:
            Ruta completa al archivo de audio
        """
        return os.path.join(self.cache_dir, f"{cache_key}.mp3")
    
    async def get_from_cache(self, text: str, voice_id: str, language: str = "es") -> Optional[str]:
        """
        Busca un archivo de audio en el caché.
        
        Args:
            text: Texto original
            voice_id: ID de la voz
            language: Idioma del texto
            
        Returns:
            Ruta al archivo de audio si existe en caché, None en caso contrario
        """
        if not self.enabled:
            return None
        
        try:
            # Generar clave de caché
            cache_key = self._generate_cache_key(text, voice_id, language)
            file_path = self._get_file_path(cache_key)
            
            # Verificar si existe en el sistema de archivos
            if not os.path.exists(file_path):
                return None
            
            # Cargar metadatos
            metadata = self._load_metadata()
            
            # Verificar si está en metadatos
            if cache_key not in metadata["files"]:
                # Si existe el archivo pero no está en metadatos, actualizar metadatos
                file_size = os.path.getsize(file_path)
                metadata["files"][cache_key] = {
                    "path": file_path,
                    "size": file_size,
                    "created_at": datetime.now().isoformat(),
                    "last_accessed": datetime.now().isoformat(),
                    "access_count": 1,
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "voice_id": voice_id,
                    "language": language,
                }
                metadata["total_size"] += file_size
                self._save_metadata(metadata)
                return file_path
            
            # Verificar si ha expirado
            file_info = metadata["files"][cache_key]
            created_at = datetime.fromisoformat(file_info["created_at"])
            if datetime.now() - created_at > timedelta(seconds=self.cache_ttl):
                # Eliminar archivo expirado
                await self.remove_from_cache(cache_key)
                return None
            
            # Actualizar metadatos de acceso
            metadata["files"][cache_key]["last_accessed"] = datetime.now().isoformat()
            metadata["files"][cache_key]["access_count"] += 1
            self._save_metadata(metadata)
            
            logger.info(f"Audio encontrado en caché: {cache_key}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error al buscar audio en caché: {str(e)}")
            return None
    
    async def save_to_cache(self, text: str, voice_id: str, audio_data: bytes, language: str = "es") -> str:
        """
        Guarda un archivo de audio en el caché.
        
        Args:
            text: Texto original
            voice_id: ID de la voz
            audio_data: Datos binarios del audio
            language: Idioma del texto
            
        Returns:
            Ruta al archivo guardado
        """
        if not self.enabled:
            return ""
        
        try:
            # Generar clave de caché
            cache_key = self._generate_cache_key(text, voice_id, language)
            file_path = self._get_file_path(cache_key)
            
            # Verificar si ya existe
            if os.path.exists(file_path):
                return file_path
            
            # Verificar espacio disponible y limpiar si es necesario
            await self._cleanup_if_needed(len(audio_data))
            
            # Guardar archivo
            with open(file_path, "wb") as f:
                f.write(audio_data)
            
            # Actualizar metadatos
            metadata = self._load_metadata()
            file_size = os.path.getsize(file_path)
            
            metadata["files"][cache_key] = {
                "path": file_path,
                "size": file_size,
                "created_at": datetime.now().isoformat(),
                "last_accessed": datetime.now().isoformat(),
                "access_count": 0,
                "text": text[:100] + "..." if len(text) > 100 else text,
                "voice_id": voice_id,
                "language": language,
            }
            
            metadata["total_size"] += file_size
            self._save_metadata(metadata)
            
            logger.info(f"Audio guardado en caché: {cache_key} ({file_size} bytes)")
            return file_path
            
        except Exception as e:
            logger.error(f"Error al guardar audio en caché: {str(e)}")
            return ""
    
    async def save_file_to_cache(self, text: str, voice_id: str, file: UploadFile, language: str = "es") -> str:
        """
        Guarda un archivo de audio subido en el caché.
        
        Args:
            text: Texto original
            voice_id: ID de la voz
            file: Archivo subido
            language: Idioma del texto
            
        Returns:
            Ruta al archivo guardado
        """
        if not self.enabled:
            return ""
        
        try:
            # Leer contenido del archivo
            contents = await file.read()
            
            # Guardar en caché
            return await self.save_to_cache(text, voice_id, contents, language)
            
        except Exception as e:
            logger.error(f"Error al guardar archivo en caché: {str(e)}")
            return ""
    
    async def remove_from_cache(self, cache_key: str) -> bool:
        """
        Elimina un archivo de audio del caché.
        
        Args:
            cache_key: Clave única del caché
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        if not self.enabled:
            return False
        
        try:
            file_path = self._get_file_path(cache_key)
            
            # Verificar si existe
            if not os.path.exists(file_path):
                return False
            
            # Eliminar archivo
            os.remove(file_path)
            
            # Actualizar metadatos
            metadata = self._load_metadata()
            
            if cache_key in metadata["files"]:
                file_size = metadata["files"][cache_key]["size"]
                metadata["total_size"] -= file_size
                del metadata["files"][cache_key]
                self._save_metadata(metadata)
            
            logger.info(f"Audio eliminado de caché: {cache_key}")
            return True
            
        except Exception as e:
            logger.error(f"Error al eliminar audio de caché: {str(e)}")
            return False
    
    async def _cleanup_if_needed(self, new_file_size: int):
        """
        Limpia el caché si es necesario para hacer espacio para un nuevo archivo.
        
        Args:
            new_file_size: Tamaño del nuevo archivo a guardar
        """
        if not self.enabled:
            return
        
        try:
            metadata = self._load_metadata()
            
            # Verificar si es necesario limpiar
            if metadata["total_size"] + new_file_size <= self.max_cache_size:
                return
            
            logger.info(f"Limpiando caché de audio para hacer espacio ({new_file_size} bytes)")
            
            # Ordenar archivos por fecha de último acceso (más antiguos primero)
            files_by_access = sorted(
                metadata["files"].items(),
                key=lambda x: (
                    datetime.fromisoformat(x[1]["last_accessed"]),
                    -x[1]["access_count"]
                )
            )
            
            # Eliminar archivos hasta tener suficiente espacio
            space_needed = metadata["total_size"] + new_file_size - self.max_cache_size
            space_freed = 0
            
            for cache_key, file_info in files_by_access:
                if space_freed >= space_needed:
                    break
                
                file_path = file_info["path"]
                file_size = file_info["size"]
                
                # Eliminar archivo
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                # Actualizar metadatos
                metadata["total_size"] -= file_size
                del metadata["files"][cache_key]
                space_freed += file_size
                
                logger.info(f"Audio eliminado en limpieza: {cache_key} ({file_size} bytes)")
            
            # Guardar metadatos actualizados
            metadata["last_cleanup"] = datetime.now().isoformat()
            self._save_metadata(metadata)
            
        except Exception as e:
            logger.error(f"Error al limpiar caché de audio: {str(e)}")
    
    async def clear_cache(self) -> bool:
        """
        Limpia todo el caché de audio.
        
        Returns:
            True si se limpió correctamente, False en caso contrario
        """
        if not self.enabled:
            return False
        
        try:
            metadata = self._load_metadata()
            
            # Eliminar todos los archivos
            for cache_key, file_info in metadata["files"].items():
                file_path = file_info["path"]
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            # Reiniciar metadatos
            metadata = {
                "files": {},
                "total_size": 0,
                "last_cleanup": datetime.now().isoformat(),
            }
            self._save_metadata(metadata)
            
            logger.info("Caché de audio limpiado completamente")
            return True
            
        except Exception as e:
            logger.error(f"Error al limpiar caché de audio: {str(e)}")
            return False
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del caché de audio.
        
        Returns:
            Diccionario con estadísticas del caché
        """
        if not self.enabled:
            return {
                "enabled": False,
                "message": "El caché de audio está desactivado"
            }
        
        try:
            metadata = self._load_metadata()
            
            # Calcular estadísticas
            total_files = len(metadata["files"])
            total_size = metadata["total_size"]
            usage_percent = (total_size / self.max_cache_size) * 100 if self.max_cache_size > 0 else 0
            
            # Calcular distribución por voces
            voice_distribution = {}
            for file_info in metadata["files"].values():
                voice_id = file_info["voice_id"]
                if voice_id not in voice_distribution:
                    voice_distribution[voice_id] = 0
                voice_distribution[voice_id] += 1
            
            # Calcular distribución por idiomas
            language_distribution = {}
            for file_info in metadata["files"].values():
                language = file_info["language"]
                if language not in language_distribution:
                    language_distribution[language] = 0
                language_distribution[language] += 1
            
            # Calcular archivos más accedidos
            top_accessed = sorted(
                metadata["files"].items(),
                key=lambda x: x[1]["access_count"],
                reverse=True
            )[:5]
            
            top_accessed_info = [
                {
                    "text": file_info["text"],
                    "voice_id": file_info["voice_id"],
                    "access_count": file_info["access_count"],
                    "size": file_info["size"]
                }
                for cache_key, file_info in top_accessed
            ]
            
            return {
                "enabled": self.enabled,
                "total_files": total_files,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "max_size_mb": round(self.max_cache_size / (1024 * 1024), 2),
                "usage_percent": round(usage_percent, 2),
                "ttl_seconds": self.cache_ttl,
                "last_cleanup": metadata["last_cleanup"],
                "voice_distribution": voice_distribution,
                "language_distribution": language_distribution,
                "top_accessed": top_accessed_info
            }
            
        except Exception as e:
            logger.error(f"Error al obtener estadísticas de caché de audio: {str(e)}")
            return {
                "enabled": self.enabled,
                "error": str(e)
            }


# Instancia global del servicio
audio_cache_service = AudioCacheService()
