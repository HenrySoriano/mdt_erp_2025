# 🎨 CREAR ICONOS PARA PWA

Para que la PWA funcione completamente, necesitas crear iconos en diferentes tamaños.

## 📋 Tamaños Requeridos

Crea los siguientes iconos en `theme/static/images/`:

- `icon-72x72.png` (72x72 píxeles)
- `icon-96x96.png` (96x96 píxeles)
- `icon-128x128.png` (128x128 píxeles)
- `icon-144x144.png` (144x144 píxeles)
- `icon-152x152.png` (152x152 píxeles)
- `icon-192x192.png` (192x192 píxeles) ⭐ **Requerido mínimo**
- `icon-384x384.png` (384x384 píxeles)
- `icon-512x512.png` (512x512 píxeles) ⭐ **Requerido mínimo**

## 🛠️ Herramientas Recomendadas

### Opción 1: Generador Online (Más Fácil)
1. Ve a: https://realfavicongenerator.net/ o https://www.pwabuilder.com/imageGenerator
2. Sube una imagen de 512x512 píxeles
3. Descarga todos los tamaños generados
4. Colócalos en `theme/static/images/`

### Opción 2: Usar Python (Pillow)
```python
from PIL import Image

# Crea un icono base de 512x512
base_icon = Image.new('RGB', (512, 512), color='#1e40af')
# Añade tu logo aquí
# ...

# Genera todos los tamaños
sizes = [72, 96, 128, 144, 152, 192, 384, 512]
for size in sizes:
    icon = base_icon.resize((size, size), Image.Resampling.LANCZOS)
    icon.save(f'theme/static/images/icon-{size}x{size}.png')
```

### Opción 3: Usar GIMP/Photoshop
1. Crea un diseño de 512x512 píxeles
2. Exporta en diferentes tamaños según la lista anterior

## 📝 Nota Temporal

Si no tienes los iconos aún, la PWA seguirá funcionando pero:
- No se podrá instalar completamente
- El navegador mostrará advertencias
- Los iconos por defecto del navegador se usarán

**Puedes crear iconos simples temporalmente** usando un generador online o creando imágenes básicas con el color corporativo (#1e40af).

