# 🚀 Subir a GitHub

Sigue estos pasos para subir el repositorio a GitHub como repositorio público:

## 1. Crear un repositorio en GitHub

1. Accede a [github.com](https://github.com)
2. Haz clic en el icono `+` en la esquina superior derecha
3. Selecciona "New repository"
4. Nombre: `postgres-mcp` (o el que prefieras)
5. Descripción: "PostgreSQL MCP Server for VS Code"
6. Selecciona "Public"
7. **NO** inicialices con README (ya lo tenemos)
8. Haz clic en "Create repository"

## 2. Agregar el remoto y subir

Después de crear el repositorio, GitHub te mostrará instrucciones. Ejecuta estos comandos:

```bash
cd /home/rokol/repos/MCP/postgres_mcp

# Agregar el remoto (reemplaza USERNAME y REPO)
git remote add origin https://github.com/USERNAME/postgres-mcp.git

# Cambiar rama a main (GitHub usa main por defecto)
git branch -M main

# Subir al repositorio remoto
git push -u origin main
```

## 3. Configuración del repositorio (Opcional)

En GitHub, en la página del repositorio:

### Settings > General
- ✅ Public repository (ya seleccionado)
- Descripción: "PostgreSQL MCP Server for VS Code"
- Topics: `mcp`, `postgres`, `vscode`, `python`

### Settings > Code and automation > Pages
- Source: Deploy from a branch
- Branch: main
- Folder: /docs (para publicar la documentación automáticamente)

## 4. Agregar Licencia (Recomendado)

```bash
# Agregar una licencia MIT
curl https://opensource.org/licenses/MIT > LICENSE

git add LICENSE
git commit -m "Add MIT license"
git push
```

## 5. Crear un token de acceso (Para push futuro)

Si prefieres usar token en lugar de contraseña:

1. GitHub > Settings > Developer settings > Personal access tokens
2. Generar nuevo token con permisos `repo`
3. Usar el token en lugar de contraseña en push

```bash
git remote set-url origin https://TOKEN@github.com/USERNAME/postgres-mcp.git
```

## Comandos rápidos para copiar

```bash
# Completo (reemplaza USERNAME)
cd /home/rokol/repos/MCP/postgres_mcp
git remote add origin https://github.com/USERNAME/postgres-mcp.git
git branch -M main
git push -u origin main
```

## ¿Listo para hacer público?

Una vez subido a GitHub:
- ✅ El repositorio es público por defecto
- ✅ Cualquiera puede verlo y clonarlo
- ✅ Issues y Pull Requests habilitados automáticamente

¡Listo para que otros contribuyan! 🎉
