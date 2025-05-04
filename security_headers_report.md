# Informe de Encabezados de Seguridad

## http://localhost

Estado: ⚠️ **Error**: Error de conexión: HTTPConnectionPool(host='localhost', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x000001594D738CD0>: Failed to establish a new connection: [WinError 10061] No se puede establecer una conexión ya que el equipo de destino denegó expresamente dicha conexión'))

---

## Recomendaciones

Para mejorar la seguridad de tu sitio web, asegúrate de incluir los siguientes encabezados:

- `X-Content-Type-Options`: `nosniff`
- `X-Frame-Options`: `DENY`, `SAMEORIGIN`
- `X-XSS-Protection`: `1`, `1; mode=block`
- `Content-Security-Policy`: Cualquier valor apropiado
- `Strict-Transport-Security`: Cualquier valor apropiado
- `Referrer-Policy`: `no-referrer`, `no-referrer-when-downgrade`, `origin`, `origin-when-cross-origin`, `same-origin`, `strict-origin`, `strict-origin-when-cross-origin`
- `Permissions-Policy`: Cualquier valor apropiado
