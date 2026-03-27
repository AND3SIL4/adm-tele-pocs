-- Insert a new execution date
INSERT OR IGNORE INTO dates(exe_date)
VALUES ('13/03/2026');

-- Insert a new record
INSERT OR IGNORE INTO records(id_record, exe_date, state)
VALUES ('52040290-programa-saludmental-medicinageneral-teleorientación', '13/03/2026', 1);

-- Create a query to search if the record exists
SELECT 1
FROM records
WHERE exe_date = '13/03/2026' 
AND id_record = '100023494RESS';

-- Select the date to know if there is any record
SELECT exe_date
FROM dates
ORDER BY start_date ASC;

-- Validate if the tables were created
SELECT 1
FROM sqlite_master
WHERE type = 'table'
AND name = 'dates'; -- table name

-- Query to get the accuracy of the records
SELECT COUNT(*)
FROM records
WHERE state = 1;

SELECT COUNT(*)
FROM records;

SELECT COUNT(*)
FROM records
WHERE state = 2;

-- Delte the date record after finish validations
DELETE
FROM dates
WHERE exe_date = '13/03/2026'