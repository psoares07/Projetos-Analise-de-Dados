-- Tabela de Medições (Fato)
CREATE TABLE IF NOT EXISTS tb_medicoes (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    location VARCHAR(50),
    temperature_c DECIMAL(5,2),
    humidity_pct DECIMAL(5,2),
    luminosity_raw INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Metadados
COMMENT ON TABLE tb_medicoes IS 'Tabela fato contendo leituras históricas dos sensores IoT';
COMMENT ON COLUMN tb_medicoes.luminosity_raw IS 'Valor bruto (0-4095) do sensor LDR. Requer normalização.';