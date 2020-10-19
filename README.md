Backup:
- create backup/[Checking,Credit_Card, Money_Market].csv
-- This is just the data as it came from bank
- create backup/[nameMappings, tagNameMappings].csv
-- nameMapping = Description -> Name  (exact match?)
-- tagNameMapping = Name -> tag

Restore:
- clears out db
-- drop_all, create_all
-- create accountTypes, create Categories - hardcoded in setup.py for now
- reads in all 5 files applying name/tag mappings to account entries
