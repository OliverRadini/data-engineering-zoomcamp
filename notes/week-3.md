# Week 3

## OLAP vs OLTP

| Category | OLTP | OLAP |
|----------|------|------|
| Purpose  | Control and run essential business operations | Support decisions, show hidden insights |
| Data updates | Short, fast, triggered by user | Periodically refreshed according to a schedule |
| Database design | Normalised | Denormalised |
| Space requirements | Generally small if historical data is archived | Generally large due to aggregating large datasets |
| Backup and recovery | Regular backups to ensure continuity | Lost data can be reloaded from OLTP |
| Productivity | Increases productivity of end users | Increases productivity of business maangers/executives/analysts |
| User examples | Customer facing personnel, clerks, online shoppers | Analysts and executives |