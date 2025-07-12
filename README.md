# Sistema de Búsqueda Inteligente con Agente React

Este proyecto implementa un sistema de búsqueda inteligente que utiliza un **agente React** con **Gemini LLM** para analizar consultas y decidir automáticamente la mejor estrategia de búsqueda.

## 🏗️ Arquitectura

### Patrón React (Reasoning and Acting)

El sistema implementa el patrón React que combina:

1. **Reasoning**: Análisis inteligente de consultas usando Gemini LLM
2. **Acting**: Ejecución de la estrategia de búsqueda más apropiada
3. **Evaluation**: Evaluación y mejora de resultados

### Componentes Principales

```
vector-portable/
├── config.py              # Configuración centralizada
├── search_strategies.py   # Estrategias de búsqueda
├── react_agent.py        # Agente React con Gemini
├── semantic_search.py    # Interfaz principal
└── requirements.txt      # Dependencias
```

## 🎯 Estrategias de Búsqueda

### 1. EXACT_MATCH
- **Uso**: Nombres específicos, números ADD, registros de aeronave
- **Ejemplo**: "Ortega", "ADD-001", "EC-MAA"
- **Confianza**: Alta (1.0)

### 2. CLASSIC
- **Uso**: Términos técnicos específicos, códigos
- **Ejemplo**: "landing light", "brake system", "electrical panel"
- **Confianza**: Media-Alta (0.6-1.0)

### 3. SEMANTIC
- **Uso**: Conceptos, problemas, lenguaje natural
- **Ejemplo**: "problemas de frenos", "defectos eléctricos"
- **Confianza**: Variable (basada en similitud)

### 4. HYBRID
- **Uso**: Consultas complejas con múltiples aspectos
- **Ejemplo**: "problemas de motor en EC-MAA"
- **Confianza**: Combinada de múltiples estrategias

## 🚀 Instalación

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
Crear archivo `.env`:
```env
# Base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=midb
DB_USER=admin
DB_PASSWORD=admin123

# Gemini LLM (opcional pero recomendado)
GEMINI_API_KEY=tu_api_key_aqui

# Configuración de búsqueda
SEARCH_TOP_K=5
SEARCH_MAX_TOP_K=20
SIMILARITY_THRESHOLD=0.3

# Logging
LOG_LEVEL=INFO
ENABLE_GEMINI=true
```

### 3. Configurar base de datos
Asegúrate de que PostgreSQL esté ejecutándose con pgvector habilitado.

## 🎮 Uso

### Ejecutar el sistema
```bash
python semantic_search.py
```

### Ejemplos de consultas

#### Búsqueda por técnico
```
Consulta: "Ortega"
Estrategia: EXACT_MATCH
```

#### Búsqueda por defecto específico
```
Consulta: "landing light"
Estrategia: CLASSIC
```

#### Búsqueda semántica
```
Consulta: "problemas de frenos"
Estrategia: SEMANTIC
```

#### Búsqueda híbrida
```
Consulta: "defectos eléctricos en EC-MAA"
Estrategia: HYBRID
```

## 🤖 Agente React

### Análisis de Consulta
El agente analiza cada consulta considerando:
- Tipo de consulta (nombre, número, problema técnico)
- Especificidad (exacta vs. semántica)
- Campos relevantes
- Complejidad

### Decisión de Estrategia
```python
# Ejemplo de análisis
analysis = agent.analyze_query("Ortega")
print(f"Estrategia: {analysis.strategy}")
print(f"Confianza: {analysis.confidence}")
print(f"Razonamiento: {analysis.reasoning}")
```

### Sugerencias de Mejora
El agente puede sugerir mejoras para consultas que obtienen pocos resultados:
```python
suggestions = agent.suggest_query_improvements(query, results)
```

## 📊 Características

### ✅ Ventajas de la nueva arquitectura

1. **Modularidad**: Cada estrategia está separada y es extensible
2. **Inteligencia**: Gemini analiza consultas de forma inteligente
3. **Flexibilidad**: Múltiples estrategias combinables
4. **Robustez**: Fallbacks automáticos si una estrategia falla
5. **Configurabilidad**: Todo configurable via variables de entorno
6. **Observabilidad**: Logging detallado y estadísticas

### 🔄 Flujo de trabajo

```
Usuario → Consulta → Agente React → Análisis → Estrategia → Búsqueda → Resultados
                ↓
        [Evaluación y mejora]
                ↓
        [Sugerencias si es necesario]
```

## 🛠️ Desarrollo

### Agregar nueva estrategia
1. Crear clase en `search_strategies.py`
2. Implementar método `search()`
3. Agregar al `SearchStrategyFactory`

### Modificar análisis
1. Editar `_build_analysis_prompt()` en `react_agent.py`
2. Ajustar `_parse_gemini_response()`

### Configuración avanzada
- Modificar `config.py` para nuevas opciones
- Usar variables de entorno para configuración dinámica

## 📈 Monitoreo

### Estadísticas del sistema
```python
stats = agent.get_search_statistics()
print(f"Gemini disponible: {stats['gemini_available']}")
print(f"Estrategias: {stats['strategies_available']}")
```

### Logging
El sistema registra:
- Análisis de consultas
- Estrategias seleccionadas
- Resultados de búsqueda
- Errores y fallbacks

## 🔧 Troubleshooting

### Error: "No se configuró Gemini"
- Configura `GEMINI_API_KEY` en variables de entorno
- El sistema funcionará con análisis básico

### Error: "Connection refused"
- Verifica que PostgreSQL esté ejecutándose
- Revisa configuración de base de datos

### Pocos resultados
- Usa consultas más específicas
- Revisa las sugerencias del agente
- Considera usar búsqueda híbrida

## 🎯 Próximas mejoras

- [ ] Interfaz web con Streamlit
- [ ] Cache de embeddings
- [ ] Análisis de sentimientos
- [ ] Búsqueda por fechas
- [ ] Exportación de resultados
- [ ] Métricas de rendimiento 