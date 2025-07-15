#!/usr/bin/env python3
"""
Sistema de búsqueda inteligente usando LangChain SQL Database Agent.
Basado en el patrón de Medium para SQL Database Agents.
"""

import os
import psycopg2
from typing import List, Dict
from dataclasses import dataclass
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from sentence_transformers import SentenceTransformer
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate

# Cargar variables de entorno
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Archivo .env cargado")
except ImportError:
    print("⚠️  python-dotenv no instalado")

@dataclass
class SearchResult:
    """Resultado de búsqueda simplificado."""
    add_number: str
    aircraft: str
    discrepancy: str
    technician: str
    similarity: float

class SemanticSearchTool:
    """Herramienta para búsqueda semántica con embeddings."""
    
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', '5432')),
            'database': os.getenv('DB_NAME', 'midb'),
            'user': os.getenv('DB_USER', 'admin'),
            'password': os.getenv('DB_PASSWORD', 'admin123')
        }
    
    def semantic_search(self, query: str) -> str:
        """Búsqueda semántica por conceptos usando embeddings."""
        try:
            query_embedding = self.embedding_model.encode(query)
            query_embedding_list = query_embedding.tolist()
            
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()
            
            try:
                cur.execute("""
                    SELECT add_number, aircraft_registration, discrepancy, technician,
                           1 - (embedding <=> %s::vector) as similarity
                    FROM documentos 
                    WHERE embedding IS NOT NULL
                    ORDER BY embedding <=> %s::vector LIMIT 5
                """, (query_embedding_list, query_embedding_list))
                
                results = []
                for row in cur.fetchall():
                    results.append(f"ADD: {row[0]}, Aeronave: {row[1]}, Defecto: {row[2]}, Técnico: {row[3]}, Similitud: {row[4]:.3f}")
                
                if not results:
                    return "No se encontraron resultados para tu consulta."
                return f"Encontrados {len(results)} resultados:\n" + "\n".join(results)
                
            finally:
                cur.close()
                conn.close()
        except Exception as e:
            return f"Error en búsqueda semántica: {e}"

class LangChainSearchAgent:
    """Agente de búsqueda usando LangChain con herramientas SQL y semánticas."""
    
    def __init__(self):
        # Configurar Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("⚠️  GEMINI_API_KEY no configurada")
            self.llm = None
            return
        
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=api_key,
                temperature=0.0,
                max_output_tokens=500
            )
            print("✅ Gemini configurado correctamente")
        except Exception as e:
            print(f"❌ Error configurando Gemini: {e}")
            self.llm = None
            return
        
        # Configurar conexión a la base de datos
        db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', '5432')),
            'database': os.getenv('DB_NAME', 'midb'),
            'user': os.getenv('DB_USER', 'admin'),
            'password': os.getenv('DB_PASSWORD', 'admin123')
        }
        
        try:
            # Crear conexión SQLDatabase para LangChain
            connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
            self.db = SQLDatabase.from_uri(connection_string)
            print("✅ Conexión a base de datos establecida")
        except Exception as e:
            print(f"❌ Error conectando a la base de datos: {e}")
            self.db = None
            return
        
        # Configurar SQL Database Toolkit
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        
        # Configurar herramienta de búsqueda semántica
        self.semantic_tool = SemanticSearchTool()
        
        # Combinar herramientas SQL con búsqueda semántica
        sql_tools = self.toolkit.get_tools()
        semantic_tool = Tool(
            name="semantic_search",
            description="Buscar por conceptos técnicos usando embeddings semánticos. Usa para: smoke detector, landing light problems, engine issues, problemas técnicos",
            func=self.semantic_tool.semantic_search
        )
        
        self.tools = sql_tools + [semantic_tool]
        
        # Prompt específico para el agente
        self.prompt = PromptTemplate.from_template("""
        Eres un asistente experto en búsqueda de documentos de mantenimiento de aeronaves.
        
        Tienes acceso a una base de datos PostgreSQL con la tabla "documentos" que contiene:
        - add_number: Número del ADD
        - aircraft_registration: Matrícula de la aeronave  
        - discrepancy: Descripción del defecto
        - technician: Nombre del técnico
        - notes: Notas adicionales
        - corrective_action: Acción correctiva
        - embedding: Vector de embeddings (para búsqueda semántica)
        
        Herramientas disponibles:
        {tools}
        
        Nombres de herramientas: {tool_names}
        
        REGLAS IMPORTANTES:
        1. Para búsquedas específicas (ADD, técnico, aeronave) usa las herramientas SQL
        2. Para conceptos técnicos (problemas, sistemas) usa semantic_search
        3. SIEMPRE usa el formato: "Thought:", "Action:", "Action Input:"
        4. Después de obtener resultados, da una "Final Answer" clara
        5. Si no encuentras resultados, indícalo claramente
        
        EJEMPLOS DE USO:
        - "ADD-002" → sql_db_query con SELECT * FROM documentos WHERE add_number LIKE '%ADD-002%'
        - "Ortega" → sql_db_query con SELECT * FROM documentos WHERE technician LIKE '%Ortega%'
        - "smoke detector" → semantic_search
        - "landing light problems" → semantic_search
        - "problemas de motor" → semantic_search
        
        IMPORTANTE:
        - SOLO puedes responder usando la información que te da la herramienta
        - Si no hay resultados, responde: "No se encontraron resultados para tu consulta."
        - NUNCA inventes resultados
        - SIEMPRE usa la tabla "documentos" para queries SQL
        
        Consulta del usuario: {input}
        
        {agent_scratchpad}
        """)
        
        # Crear agente con todas las herramientas
        if self.llm and self.db:
            self.agent = create_react_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=self.prompt
            )
            self.agent_executor = AgentExecutor(
                agent=self.agent,
                tools=self.tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=3
            )
        else:
            self.agent_executor = None
    
    def search(self, query: str) -> str:
        """Ejecutar búsqueda con el agente."""
        if not self.agent_executor:
            return "❌ Error: No se pudo configurar el agente. Verifica GEMINI_API_KEY y la conexión a la base de datos."
        
        try:
            result = self.agent_executor.invoke({"input": query})
            return result["output"]
        except Exception as e:
            # Si es error de cuota, sugerir usar búsqueda directa
            if "429" in str(e) or "quota" in str(e).lower():
                return f"❌ Error: Cuota de Gemini excedida. {e}\n\n💡 Sugerencia: Usa 'python simple_search.py' para búsquedas directas sin LLM."
            return f"❌ Error en la búsqueda: {e}"

def main():
    """Interfaz principal simplificada."""
    print("🤖 BÚSQUEDA INTELIGENTE CON LANGCHAIN SQL AGENT")
    print("="*60)
    
    # Inicializar agente
    agent = LangChainSearchAgent()
    
    if not agent.agent_executor:
        print("❌ No se pudo configurar el agente")
        print("💡 Verifica GEMINI_API_KEY y la conexión a la base de datos")
        return
    
    print("\n🎯 EJEMPLOS DE CONSULTAS:")
    print("• 'Busca ADD-002'")
    print("• '¿Qué problemas de smoke detector hay?'")
    print("• 'Muestra los ADD de Ortega'")
    print("• 'Problemas de landing light'")
    print("• '¿Cuántos documentos tiene el técnico Medina?'")
    
    while True:
        print("\n" + "="*60)
        query = input("🔍 Consulta (o 'salir'): ").strip()
        
        if query.lower() in ['salir', 'exit', 'quit']:
            print("¡Hasta luego! 👋")
            break
        
        if not query:
            print("❌ La consulta no puede estar vacía")
            continue
        
        print(f"\n🔍 Buscando: '{query}'")
        print("-" * 60)
        
        result = agent.search(query)
        print(f"\n📋 RESULTADO:")
        print(result)
        print("-" * 60)

if __name__ == "__main__":
    main() 