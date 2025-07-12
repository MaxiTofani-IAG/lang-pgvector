CREATE TABLE documentos (
    id SERIAL PRIMARY KEY,
    add_number VARCHAR(50),                -- Número identificador del ADD
    aircraft_registration VARCHAR(20),     -- Matrícula de la aeronave
    msn VARCHAR(50),                       -- Número de serie del fabricante
    date_reported DATE,                    -- Fecha de detección
    discrepancy TEXT,                      -- Descripción del defecto
    ata_chapter VARCHAR(10),               -- Capítulo ATA
    deferral_category VARCHAR(10),         -- Categoría MEL (A/B/C/D)
    expiry_date DATE,                      -- Fecha límite del diferimiento
    status VARCHAR(20),                    -- Ej. 'Open', 'Closed'
    corrective_action TEXT,                -- Acción correctiva (si aplica)
    technician VARCHAR(100),               -- Técnico responsable
    station VARCHAR(50),                   -- Estación o aeropuerto
    notes TEXT,                           -- Notas adicionales
    embedding vector(384)                  -- Para búsqueda semántica
);