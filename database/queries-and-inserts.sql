-- Insert a new execution date
INSERT INTO dates(exe_date)
VALUES ('12/03/2026');

-- Insert a new record
INSERT OR IGNORE INTO records(id_record, exe_date)
VALUES ('100023494RESS', '12/03/2026');

-- Create a query to search if the record exists
SELECT 1
FROM records
WHERE exe_date = '12/03/2026' 
AND id_record = '100023494RESS';

-- Select the date to know if there is any record
SELECT 1
FROM dates
WHERE exe_date = '13/03/2026'

-- Validate if the tables were created
SELECT 1
FROM sqlite_master
WHERE type = 'table'
AND name = 'dates'; -- table name


SELECT *
FROM sqlite_master;
