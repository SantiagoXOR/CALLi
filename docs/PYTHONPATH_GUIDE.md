# Guía para Configurar PYTHONPATH en CALLi

Este documento proporciona instrucciones detalladas sobre cómo configurar correctamente el PYTHONPATH para el proyecto CALLi, lo que es esencial para evitar errores de importación como `ModuleNotFoundError: No module named 'app.dependencies'`.

## ¿Qué es PYTHONPATH?

PYTHONPATH es una variable de entorno que Python utiliza para buscar módulos cuando se realizan importaciones. Cuando importas un módulo en tu código (por ejemplo, `import app.dependencies`), Python busca ese módulo en los directorios listados en PYTHONPATH.

## Problemas Comunes

El error más común relacionado con PYTHONPATH es:

```
ModuleNotFoundError: No module named 'app.dependencies'
```

Este error ocurre cuando Python no puede encontrar el módulo `app.dependencies` en ninguno de los directorios listados en PYTHONPATH.

## Configuración Correcta de PYTHONPATH

Para el proyecto CALLi, PYTHONPATH debe incluir:

1. El directorio raíz del proyecto (donde se encuentra el archivo `.env`)
2. El directorio `backend-call-automation`

### En Windows (CMD)

```cmd
set PYTHONPATH=%CD%;%CD%\backend-call-automation
```

### En Windows (PowerShell)

```powershell
$env:PYTHONPATH = "$PWD;$PWD\backend-call-automation"
```

### En Linux/macOS

```bash
export PYTHONPATH=$PWD:$PWD/backend-call-automation
```

## Uso de Scripts de Ayuda

Hemos proporcionado scripts para configurar automáticamente el PYTHONPATH:

- En Windows: `run_tests.bat`
- En Linux/macOS: `run_tests.sh`

Para ejecutar los tests con el PYTHONPATH configurado correctamente:

```bash
# En Windows
.\run_tests.bat

# En Linux/macOS
./run_tests.sh
```

## Configuración en IDEs

### PyCharm

1. Ve a `File > Settings > Project > Python Interpreter`
2. Haz clic en el ícono de engranaje y selecciona "Show All..."
3. Selecciona tu intérprete y haz clic en el ícono de edición
4. Ve a la pestaña "Paths"
5. Agrega tanto el directorio raíz como `backend-call-automation` a la lista

### Visual Studio Code

1. Crea o edita el archivo `.vscode/settings.json`
2. Agrega la siguiente configuración:

```json
{
    "python.analysis.extraPaths": [
        "${workspaceFolder}",
        "${workspaceFolder}/backend-call-automation"
    ]
}
```

## Verificación de la Configuración

Para verificar que PYTHONPATH está configurado correctamente:

```python
import sys
print(sys.path)
```

Deberías ver tanto el directorio raíz como `backend-call-automation` en la lista.

## Solución de Problemas

Si sigues teniendo problemas con las importaciones:

1. Verifica que todos los directorios en la ruta de importación tengan un archivo `__init__.py`
2. Asegúrate de que estás ejecutando Python desde el directorio correcto
3. Intenta instalar el paquete en modo desarrollo:

```bash
pip install -e backend-call-automation/
```

## En CI/CD

En GitHub Actions, configura PYTHONPATH en el workflow:

```yaml
- name: Set PYTHONPATH
  run: echo "PYTHONPATH=$GITHUB_WORKSPACE:$GITHUB_WORKSPACE/backend-call-automation" >> $GITHUB_ENV
```

## Conclusión

Una configuración correcta de PYTHONPATH es esencial para el funcionamiento adecuado del proyecto CALLi. Siguiendo esta guía, deberías poder resolver la mayoría de los problemas relacionados con importaciones de módulos.
