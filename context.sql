-- Create the main table to store the dates and its state
CREATE TABLE IF NOT EXISTS dates(
	exe_date TEXT PRIMARY KEY, -- Format dd/mm/yyyy
	state INTEGER NOT NULL DEFAULT 0, 
	start_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
	-- Build constraints
	CONSTRAINT chk_state CHECK(state IN(1,0)) -- 1=COMPLETE 0=PENDING
);

-- Create the main table to store the records validated
CREATE TABLE IF NOT EXISTS records(
	id_record TEXT PRIMARY KEY,
	exe_date TEXT NOT NULL,
	-- Build contraints 
	FOREIGN KEY (exe_date) 
		REFERENCES dates(exe_date)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

-- Create the indexing to increase the performance
CREATE INDEX IF NOT EXISTS idx_records_exe_date
ON records(exe_date);