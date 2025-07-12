# Búsqueda Inteligente Simplificada

Sistema de búsqueda inteligente con agente React en **un solo archivo** - fácil de entender y usar.

## 🚀 Instalación Rápida

```bash
# Instalar dependencias
pip install -r requirements_simple.txt

# Configurar variables (opcional)
export GEMINI_API_KEY="tu_api_key"
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="midb"
export DB_USER="admin"
export DB_PASSWORD="admin123"

# Ejecutar
python simple_search.py
```

## 🎯 Cómo Funciona

### 1. Análisis Inteligente
El agente analiza tu consulta y decide automáticamente la mejor estrategia:

- **EXACT**: Para nombres, números ADD, aeronaves
- **SEMANTIC**: Para conceptos y lenguaje natural  
- **HYBRID**: Para consultas complejas

### 2. Búsqueda Automática
Ejecuta la estrategia más apropiada y muestra resultados.

### 3. Interfaz Simple
Menú claro con opciones predefinidas.

## 📝 Ejemplos de Uso

```
Consulta: "Ortega"
→ Estrategia: EXACT
→ Busca en nombres de técnicos

Consulta: "landing light"  
→ Estrategia: SEMANTIC
→ Busca por similitud semántica

Consulta: "problemas de frenos"
→ Estrategia: SEMANTIC
→ Busca conceptos relacionados
```

## 🎮 Opciones del Menú

1. **🔍 Búsqueda libre** - Describe lo que buscas
2. **🎯 Por técnico** - Nombres de técnicos
3. **✈️ Por aeronave** - Registros de aeronaves
4. **🔧 Por defecto** - Términos técnicos
5. **📊 Estadísticas** - Ver configuración
6. **🚪 Salir**

## ⚙️ Configuración

### Con Gemini (Recomendado)
```bash
export GEMINI_API_KEY="tu_api_key"
```
- Análisis más inteligente
- Mejor decisión de estrategia

### Sin Gemini
- Funciona con análisis básico
- Reglas simples para decidir estrategia

### Base de Datos
```bash
export DB_HOST="localhost"
export DB_PORT="5432" 
export DB_NAME="midb"
export DB_USER="admin"
export DB_PASSWORD="admin123"
```

## 🔧 Troubleshooting

### Error de conexión a BD
```bash
# Verificar PostgreSQL
docker-compose up -d
```

### Error con Gemini
- El sistema funciona sin Gemini
- Usa análisis básico automáticamente

### Pocos resultados
- Usa términos más específicos
- Prueba diferentes categorías

## 📊 Ventajas de la Versión Simplificada

✅ **Un solo archivo** - Fácil de entender  
✅ **Configuración mínima** - Variables de entorno simples  
✅ **Funciona sin Gemini** - Análisis básico incluido  
✅ **Interfaz clara** - Menú intuitivo  
✅ **Logging detallado** - Ve qué está pasando  
✅ **Fácil de modificar** - Código simple y directo  

## 🎯 Diferencias con la Versión Compleja

| Aspecto | Compleja | Simplificada |
|---------|----------|--------------|
| Archivos | 6 archivos | 1 archivo |
| Configuración | Compleja | Simple |
| Dependencias | Muchas | Mínimas |
| Flexibilidad | Alta | Media |
| Facilidad | Compleja | Simple |

## 🚀 Próximos Pasos

1. **Probar el sistema**: `python simple_search.py`
2. **Configurar Gemini** (opcional): Para mejor análisis
3. **Personalizar**: Modificar `simple_search.py` según necesidades
4. **Escalar**: Migrar a versión completa si se necesita más funcionalidad 