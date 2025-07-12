# 🔍 Sistema de Búsqueda Inteligente con LangChain

Sistema simplificado de búsqueda de documentos de mantenimiento de aeronaves usando **LangChain React Agents** y **Gemini**.

## 🚀 Características

- **LangChain React Agents**: Agente inteligente que decide automáticamente qué tipo de búsqueda usar
- **Búsqueda Exacta**: Para ADD específicos, técnicos, aeronaves
- **Búsqueda Semántica**: Para conceptos técnicos y problemas
- **Gemini Integration**: Análisis inteligente de consultas
- **Interfaz Simple**: Fácil de usar y entender

## 📦 Instalación

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements_simple.txt
   ```

2. **Configurar variables de entorno:**
   ```bash
   # Copiar archivo de ejemplo
   cp env_example.txt .env
   
   # Editar .env y agregar tu API key de Gemini
   GEMINI_API_KEY=tu_api_key_aqui
   ```

3. **Ejecutar:**
   ```bash
   python langchain_search.py
   ```

## 🎯 Ejemplos de Uso

### Búsquedas Exactas
```
🔍 Consulta: Busca ADD-002
🔍 Consulta: Muestra los ADD de Ortega
🔍 Consulta: Aeronave EC-MAA
```

### Búsquedas Semánticas
```
🔍 Consulta: ¿Qué problemas de smoke detector hay?
🔍 Consulta: Problemas de landing light
🔍 Consulta: Engine failures
```

## 🧠 Cómo Funciona

1. **Análisis de Consulta**: El agente analiza tu consulta
2. **Decisión Inteligente**: Decide si usar búsqueda exacta o semántica
3. **Ejecución**: Ejecuta la búsqueda apropiada
4. **Resultado**: Te muestra los resultados de forma clara

## 🛠️ Estructura del Proyecto

```
vector-portable/
├── langchain_search.py    # Sistema principal con LangChain
├── requirements_simple.txt # Dependencias
├── env_example.txt        # Ejemplo de configuración
└── README_langchain.md    # Este archivo
```

## 🔧 Configuración

### Variables de Entorno (.env)
```bash
# Base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=midb
DB_USER=admin
DB_PASSWORD=admin123

# Gemini API
GEMINI_API_KEY=tu_api_key_aqui
```

## 🎉 Ventajas del Sistema Simplificado

- ✅ **Fácil de entender**: Código claro y directo
- ✅ **LangChain**: Framework estándar y confiable
- ✅ **React Agents**: Decisión automática de estrategia
- ✅ **Gemini**: Análisis inteligente de consultas
- ✅ **POC Ready**: Perfecto para demostraciones

## 🚀 Próximos Pasos

1. Configura tu API key de Gemini
2. Ejecuta `python langchain_search.py`
3. ¡Prueba diferentes tipos de consultas!
4. Personaliza según tus necesidades

---

**¡Simple, inteligente y efectivo!** 🎯 