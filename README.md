# Timetable Generator

A Python-based academic course timetable generator that creates non-conflicting schedules while handling various constraints like exam clashes and credit limits.

## Features

- Automated timetable generation considering:
  - Time slot conflicts
  - Midsem exam schedules
  - Comprehensive exam schedules
  - Total credit limits (≤25)
- Support for multiple section types (Lectures/Tutorials/Practicals)
- Generates up to 50 possible valid timetables
- Sorted output based on slot timing

## Repository Structure
```
.
├── main_code.py            # Core timetable generation logic
├── rows_remover.py         # Excel data preprocessing 
├── Timetable_27_Dec_2024.pdf
├── Timetable_27_Dec_2024_removed.pdf
├── Timetable_27_Dec_2024_removed_removed.pdf
├── Timetable_27_Dec_2024_removed_removed.xlsx
└── Timetable_27_Dec_2024_removed_removed_rows_removed.xlsx
```

## Prerequisites
- Python 3.x
- pandas

## Setup
```bash
git clone https://github.com/SubhamPan/Timetable-Generator.git
cd Timetable-Generator
pip install pandas
```

## Usage
```bash
python main_code.py
```

Follow the prompts to input:
1. Number of courses
2. Course IDs

## Example Course Sets
```python
# CDCs: CS F303, CS F363, CS F364
# Full load: CS F303, CS F363, CS F364, MATH F243, ECON F354, CS F320
# An example of clash: MATH F243, CS F407
```

## Error Handling
- Course ID validation
- Duplicate detection
- Credit limit checks
- Conflict detection

## License
[MIT License](LICENSE)

## What next?
Output midsem and compre schedule if a timetable generation is possible. This is easy to do, I am just lazy.
If anyone wants to contribute to the frontend and perhaps display the generated timetables, drop an email at f20220141@pilani.bits-pilani.ac.in

