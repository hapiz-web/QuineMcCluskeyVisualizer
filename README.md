# Quine-McCluskey Visualizer

A modern Django web application for visualizing the Quine-McCluskey minimization process step by step. It helps users simplify Boolean expressions interactively while showing the grouping, combination iterations, prime implicants, chart, essential implicants, Petrick method, and final expression in a clear, educational interface.

## Description

The Quine-McCluskey Visualizer is designed for students and learners who want to understand Boolean simplification in a more intuitive way. Instead of only returning a final minimized expression, the app explains how the result is derived through each logical step.

## Features

- Step-by-step Quine-McCluskey visualization
- Initial grouping display
- Combination iteration visualization
- Prime implicant table and chart
- Essential prime implicant detection
- Petrick method walkthrough
- Final Boolean expression display
- Input validation for duplicates, overlaps, and out-of-range values
- Responsive Bootstrap 5 interface
- Calculation history with view/delete options
- Statistics card for solver metrics

## Screenshots

Screenshots can be added to the project documentation folder once available. The app is designed to display:

- the input form
- the step-by-step simplification result
- the statistics panel
- the history page

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

## How to Run

Start the development server:

```bash
python manage.py runserver
```

Then open your browser at:

```text
http://127.0.0.1:8000/
```

## Project Structure

```text
project/
├── qm/                  # Django app for forms, views, and logic integration
├── quinemccluskey/      # Project settings and URL configuration
├── templates/           # HTML templates for the UI
├── static/              # CSS and JavaScript assets
├── docs/                # Project documentation
├── media/               # Uploaded or generated media files
├── db.sqlite3           # SQLite database
└── manage.py            # Django management script
```

## Algorithm Workflow

The application follows this workflow:

1. Parse and validate input values
2. Group minterms by the number of 1s in binary form
3. Repeatedly combine compatible terms
4. Collect prime implicants
5. Build the prime implicant chart
6. Identify essential prime implicants
7. Apply the Petrick method if needed
8. Generate the final simplified Boolean expression

## Technologies

- Python
- Django
- Bootstrap 5
- SQLite
- HTML/CSS/JavaScript

## Future Improvements

- Add export to PDF or image
- Improve chart styling and animations
- Support more advanced Boolean examples
- Add dark mode
- Add unit tests for more solver cases

## Author

Jarvis
