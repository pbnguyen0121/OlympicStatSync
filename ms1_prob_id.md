# Milestone 1 Problem Identification

## 1. Issues in the Original Data Files

### olympic_athlete_bio.csv -PB
- Many lines are missing `born` (DOB) values
- Many lines are missing `weight`

**Planned Solution**:
- Leave age as blank if DOB is missing when writing event results
- Missing weight data will be ignored for now

### olympic_athlete_event_results.csv -PB
- Some event results are incomplete or missing
- Duplicate athlete IDs can occur across different events

**Planned Solution**:
- Ensure every row has a valid athlete ID and event ID