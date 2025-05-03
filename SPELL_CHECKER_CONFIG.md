# Configuración del Verificador Ortográfico

Este proyecto utiliza [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker) para verificar la ortografía en el código. Como el proyecto contiene texto en español e inglés, hemos configurado el verificador para soportar ambos idiomas.

## Extensiones Requeridas

Para que la verificación ortográfica funcione correctamente, necesitas instalar las siguientes extensiones de VS Code:

1. **Code Spell Checker** - Verificador ortográfico base
   ```
   code --install-extension streetsidesoftware.code-spell-checker
   ```

2. **Spanish - Code Spell Checker** - Diccionario español
   ```
   code --install-extension streetsidesoftware.code-spell-checker-spanish
   ```

## Configuración

La configuración del verificador ortográfico se encuentra en los siguientes archivos:

- `.vscode/settings.json` - Configuración específica para VS Code
- `cspell.json` - Configuración general del verificador ortográfico
- `technical-terms.txt` - Diccionario personalizado con términos técnicos

### Añadir Palabras al Diccionario

Si encuentras palabras que son marcadas como errores pero son correctas (por ejemplo, términos técnicos específicos del proyecto), puedes:

1. **Añadir la palabra al diccionario del espacio de trabajo**:
   - Coloca el cursor sobre la palabra marcada como error
   - Presiona `Ctrl+.` (Windows/Linux) o `Cmd+.` (Mac)
   - Selecciona "Add to workspace dictionary"

2. **Añadir la palabra al diccionario personalizado**:
   - Añade la palabra al archivo `technical-terms.txt`

## Solución de Problemas

Si el verificador ortográfico sigue marcando palabras en español como errores después de instalar las extensiones y configurar el proyecto:

1. Reinicia VS Code
2. Verifica que las extensiones estén instaladas correctamente
3. Asegúrate de que la configuración en `.vscode/settings.json` incluya `"cSpell.language": "en,es"`
