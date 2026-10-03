"""Utilidades para operaciones con archivos."""

import os
import tempfile
from pathlib import Path
from typing import Any, BinaryIO, Optional, TextIO, Union


def ensure_dir(directory: Union[str, Path]) -> Path:
    """Asegura que un directorio exista, creándolo si es necesario.
    
    Args:
        directory: Ruta al directorio.
        
    Returns:
        Objeto Path del directorio.
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def create_temp_file(
    content: str = "",
    suffix: str = None,
    prefix: str = None,
    dir: Union[str, Path] = None,
    text: bool = True,
    encoding: str = 'utf-8',
    delete: bool = True
) -> str:
    """Crea un archivo temporal con el contenido especificado.
    
    Args:
        content: Contenido del archivo.
        suffix: Sufijo para el nombre del archivo.
        prefix: Prefijo para el nombre del archivo.
        dir: Directorio donde crear el archivo.
        text: Si es True, abre el archivo en modo texto.
        encoding: Codificación del archivo.
        delete: Si es True, el archivo se eliminará al cerrarse.
        
    Returns:
        Ruta al archivo temporal creado.
    """
    mode = 'w+' if text else 'w+b'
    
    with tempfile.NamedTemporaryFile(
        mode=mode,
        suffix=suffix or '',
        prefix=prefix or 'tmp',
        dir=str(dir) if dir else None,
        encoding=encoding if text else None,
        delete=delete
    ) as temp_file:
        if content:
            if text:
                temp_file.write(content)
            else:
                temp_file.write(content.encode(encoding) if isinstance(content, str) else content)
            temp_file.flush()
        
        return temp_file.name


def read_file(
    file_path: Union[str, Path],
    binary: bool = False,
    encoding: str = 'utf-8'
) -> Union[str, bytes]:
    """Lee el contenido de un archivo.
    
    Args:
        file_path: Ruta al archivo.
        binary: Si es True, lee el archivo en modo binario.
        encoding: Codificación del archivo (solo para modo texto).
        
    Returns:
        Contenido del archivo como cadena o bytes.
    """
    mode = 'rb' if binary else 'r'
    
    with open(file_path, mode, encoding=None if binary else encoding) as f:
        return f.read()


def write_file(
    file_path: Union[str, Path],
    content: Union[str, bytes],
    binary: bool = False,
    encoding: str = 'utf-8',
    append: bool = False
) -> None:
    """Escribe contenido en un archivo.
    
    Args:
        file_path: Ruta al archivo.
        content: Contenido a escribir.
        binary: Si es True, escribe en modo binario.
        encoding: Codificación del archivo (solo para modo texto).
        append: Si es True, añade al final del archivo en lugar de sobrescribir.
    """
    mode = 'ab' if binary and append else 'wb' if binary else 'a' if append else 'w'
    
    with open(file_path, mode, encoding=None if binary else encoding) as f:
        if binary and isinstance(content, str):
            content = content.encode(encoding)
        f.write(content)


def get_file_extension(file_path: Union[str, Path]) -> str:
    """Obtiene la extensión de un archivo en minúsculas.
    
    Args:
        file_path: Ruta al archivo.
        
    Returns:
        Extensión del archivo sin el punto, en minúsculas.
    """
    return Path(file_path).suffix.lstrip('.').lower()
