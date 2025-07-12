-- Load data from CSV file
COPY documentos (
    add_number,
    aircraft_registration,
    date_reported,
    discrepancy,
    ata_chapter,
    deferral_category,
    expiry_date,
    status,
    corrective_action,
    technician,
    station,
    notes
) 
FROM '/docker-entrypoint-initdb.d/data/import.csv' 
WITH (FORMAT csv, HEADER true);

-- Update msn column with default values since it's not in the CSV
UPDATE documentos SET msn = 'N/A' WHERE msn IS NULL;
