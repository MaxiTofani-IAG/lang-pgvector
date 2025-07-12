#!/usr/bin/env python3
"""
Script para generar embeddings usando sentence-transformers
y actualizar la base de datos PostgreSQL con pgvector.
"""

import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'midb',
    'user': 'admin',
    'password': 'admin123'
}

def connect_db():
    """Conectar a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Error conectando a la base de datos: {e}")
        raise

def generate_embeddings():
    """Generar embeddings para todos los documentos sin embedding."""
    
    # Cargar el modelo sentence-transformers
    logger.info("Cargando modelo sentence-transformers...")
    model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensiones
    
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        # Obtener documentos sin embeddings
        logger.info("Obteniendo documentos sin embeddings...")
        cur.execute("""
            SELECT id, discrepancy, notes,corrective_action, technician, add_number 
            FROM documentos 
            WHERE embedding IS NULL
        """)
        
        documents = cur.fetchall()
        logger.info(f"Encontrados {len(documents)} documentos sin embeddings")
        
        if not documents:
            logger.info("No hay documentos que necesiten embeddings")
            return
        
        # Procesar cada documento
        for doc_id, discrepancy, notes, corrective_action, technician, add_number in documents:
            logger.info(f"Procesando documento {add_number} (ID: {doc_id})")
            
            # Combinar texto para el embedding (incluyendo technician)
            text_parts = []
            if technician:
                text_parts.append(technician)
            if discrepancy:
                text_parts.append(discrepancy)
            if notes:
                text_parts.append(notes)
            
            if not text_parts:
                logger.warning(f"Documento {add_number} no tiene texto para generar embedding")
                continue
            
            # Combinar todo el texto
            full_text = " ".join(text_parts)
            logger.info(f"Texto para embedding: {full_text[:100]}...")
            
            # Generar embedding
            embedding = model.encode(full_text)
            
            # Convertir a lista para PostgreSQL
            embedding_list = embedding.tolist()
            
            # Actualizar la base de datos
            cur.execute("""
                UPDATE documentos 
                SET embedding = %s 
                WHERE id = %s
            """, (embedding_list, doc_id))
            
            logger.info(f"Embedding generado y guardado para {add_number}")
        
        # Confirmar cambios
        conn.commit()
        logger.info("Todos los embeddings han sido generados y guardados exitosamente")
        
    except Exception as e:
        logger.error(f"Error generando embeddings: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def verify_embeddings():
    """Verificar que los embeddings se generaron correctamente."""
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        # Contar documentos con y sin embeddings
        cur.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(embedding) as con_embedding,
                COUNT(*) - COUNT(embedding) as sin_embedding
            FROM documentos
        """)
        
        total, con_embedding, sin_embedding = cur.fetchone()
        
        logger.info(f"Resumen de embeddings:")
        logger.info(f"  - Total de documentos: {total}")
        logger.info(f"  - Con embedding: {con_embedding}")
        logger.info(f"  - Sin embedding: {sin_embedding}")
        
        # Mostrar algunos ejemplos
        cur.execute("""
            SELECT add_number, discrepancy, embedding IS NOT NULL as tiene_embedding
            FROM documentos
            LIMIT 5
        """)
        
        logger.info("Ejemplos de documentos:")
        for add_number, discrepancy, tiene_embedding in cur.fetchall():
            status = "✓" if tiene_embedding else "✗"
            logger.info(f"  {status} {add_number}: {discrepancy[:50]}...")
            
    finally:
        cur.close()
        conn.close()

def clear_embeddings():
    """Limpiar todos los embeddings existentes para regenerarlos."""
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        logger.info("Limpiando embeddings existentes...")
        cur.execute("UPDATE documentos SET embedding = NULL")
        conn.commit()
        logger.info("Embeddings limpiados exitosamente")
    except Exception as e:
        logger.error(f"Error limpiando embeddings: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    logger.info("Iniciando generación de embeddings...")
    
    try:
        generate_embeddings()
        verify_embeddings()
        logger.info("Proceso completado exitosamente")
    except Exception as e:
        logger.error(f"Error en el proceso: {e}")
        exit(1) 