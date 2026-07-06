import os
import re
import base64

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT_FILE = r"D:\EZEmployee\EZEmployee_SE_Final_Report.pdf"
LOGO_SVG = r"D:\EZEmployee\jiit-logo.svg"
LOGO_PNG = r"D:\EZEmployee\jiit-logo.png"
PRELIM_PAGES = 2
MARGIN = 2 * cm
CONTENT_WIDTH = A4[0] - (2 * MARGIN)


def _register_times_new_roman():
    fonts_dir = r"C:\Windows\Fonts"
    font_files = {
        "TNR": "times.ttf",
        "TNR-Bold": "timesbd.ttf",
        "TNR-Italic": "timesi.ttf",
        "TNR-BoldItalic": "timesbi.ttf",
    }
    registered = True
    for name, filename in font_files.items():
        path = os.path.join(fonts_dir, filename)
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))
        else:
            registered = False
    return registered


HAS_TNR = _register_times_new_roman()
FONT = "TNR" if HAS_TNR else "Times-Roman"
FONT_BOLD = "TNR-Bold" if HAS_TNR else "Times-Bold"
FONT_ITALIC = "TNR-Italic" if HAS_TNR else "Times-Italic"
BLACK = colors.black


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle",
    parent=styles["Title"],
    alignment=TA_CENTER,
    fontName=FONT_BOLD,
    fontSize=16,
    leading=24,
    textColor=BLACK,
    spaceAfter=14,
))
styles.add(ParagraphStyle(
    name="CoverLine",
    parent=styles["BodyText"],
    alignment=TA_CENTER,
    fontName=FONT_BOLD,
    fontSize=18,
    leading=24,
    textColor=BLACK,
    spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="CoverSmallLine",
    parent=styles["BodyText"],
    alignment=TA_CENTER,
    fontName=FONT_BOLD,
    fontSize=16,
    leading=22,
    textColor=BLACK,
    spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="CoverLabel",
    parent=styles["BodyText"],
    fontName=FONT_BOLD,
    fontSize=14,
    leading=18,
    textColor=BLACK,
    spaceAfter=2,
))
styles.add(ParagraphStyle(
    name="CoverText",
    parent=styles["BodyText"],
    fontName=FONT,
    fontSize=12,
    leading=15,
    textColor=BLACK,
    spaceAfter=0,
))
styles.add(ParagraphStyle(
    name="ProjectRed",
    parent=styles["BodyText"],
    alignment=TA_CENTER,
    fontName=FONT_BOLD,
    fontSize=18,
    leading=24,
    textColor=colors.red,
    underline=True,
    italic=True,
    spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="H1",
    parent=styles["Heading1"],
    fontName=FONT_BOLD,
    fontSize=16,
    leading=24,
    textColor=BLACK,
    spaceBefore=10,
    spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="H2",
    parent=styles["Heading2"],
    fontName=FONT_BOLD,
    fontSize=14,
    leading=21,
    textColor=BLACK,
    spaceBefore=7,
    spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="Body",
    parent=styles["BodyText"],
    fontName=FONT,
    fontSize=12,
    leading=18,
    textColor=BLACK,
    spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="Small",
    parent=styles["BodyText"],
    fontName=FONT,
    fontSize=10.5,
    leading=15.75,
    textColor=BLACK,
    spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="Center",
    parent=styles["BodyText"],
    alignment=TA_CENTER,
    fontName=FONT,
    fontSize=12,
    leading=18,
    textColor=BLACK,
))
styles.add(ParagraphStyle(
    name="DiagramCode",
    parent=styles["Code"],
    fontName="Courier",
    fontSize=7.2,
    leading=9,
    textColor=BLACK,
))


def para(text, style="Body"):
    return Paragraph(text, styles[style])


def table(rows, widths=None, header=True, font_size=10.5):
    if widths and sum(widths) > CONTENT_WIDTH:
        scale = CONTENT_WIDTH / sum(widths)
        widths = [w * scale for w in widths]
    boxed = []
    for row in rows:
        boxed.append([
            cell if hasattr(cell, "wrap") else Paragraph(str(cell).replace("\n", "<br/>"), styles["Small"])
            for cell in row
        ])
    t = Table(boxed, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#E2E8F0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, -1), FONT),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("LEADING", (0, 0), (-1, -1), font_size + 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TEXTCOLOR", (0, 0), (-1, -1), BLACK),
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
    ]
    if header:
        commands.extend([
            ("BACKGROUND", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
            ("TEXTCOLOR", (0, 0), (-1, 0), BLACK),
        ])
    t.setStyle(TableStyle(commands))
    return t


def bullets(items):
    out = []
    for item in items:
        out.append(para(f"- {item}"))
    return out


def diagram(title, text):
    return [
        para(title, "H2"),
        Table(
            [[Preformatted(text, styles["DiagramCode"])]],
            colWidths=[CONTENT_WIDTH],
            style=TableStyle([
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#94A3B8")),
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]),
        ),
        Spacer(1, 0.12 * inch),
    ]


def page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 10)
    canvas.setFillColor(BLACK)
    # Use canvas.getPageNumber() to get the current page index reliably
    current = canvas.getPageNumber()
    if current <= PRELIM_PAGES:
        # preliminary pages use lowercase roman numerals starting at i
        page_no = _roman(current).lower()
    else:
        # main content pages start at 1 after prelim pages
        page_no = str(current - PRELIM_PAGES)
    canvas.drawCentredString(A4[0] / 2, 1.15 * cm, page_no)
    canvas.restoreState()


def _roman(number):
    pairs = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    result = []
    for value, symbol in pairs:
        while number >= value:
            result.append(symbol)
            number -= value
    return "".join(result)


def _extract_logo_png():
    if os.path.exists(LOGO_PNG):
        return LOGO_PNG
    if not os.path.exists(LOGO_SVG):
        return None
    with open(LOGO_SVG, "r", encoding="utf-8") as handle:
        svg = handle.read()
    match = re.search(r"data:image/png;base64,([^\"']+)", svg)
    if not match:
        return None
    with open(LOGO_PNG, "wb") as handle:
        handle.write(base64.b64decode(match.group(1)))
    return LOGO_PNG


def build():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        rightMargin=MARGIN,
        leftMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title="EZEmployee AI Final Project Report",
        author="EZEmployee Project Team",
    )
    story = []

    story.append(Spacer(1, 0.55 * inch))
    story.append(para("JAYPEE INSTITUTE OF INFORMATION TECHNOLOGY, NOIDA", "CoverSmallLine"))
    story.append(para("B.TECH VI SEMESTER", "CoverLine"))
    story.append(para("SOFTWARE ENGINEERING LAB", "CoverLine"))
    story.append(para("SYNOPSIS", "CoverLine"))
    story.append(para("(15B17CI573)", "CoverSmallLine"))
    story.append(Spacer(1, 0.18 * inch))
    logo_path = _extract_logo_png()
    if logo_path:
        img = Image(logo_path, width=2.25 * inch, height=3.2 * inch)
        img.hAlign = "CENTER"
        story.append(img)
    else:
        story.append(para("JIIT", "CoverTitle"))
    story.append(Spacer(1, 0.04 * inch))
    story.append(para("<u>TITLE OF PROJECT</u>", "Center"))
    story.append(para("EZEmployee", "ProjectRed"))
    story.append(Spacer(1, 0.45 * inch))
    story.append(table([
        [
            Paragraph("<b>Submission to:</b><br/>Dr.Kapil Madan", styles["CoverText"]),
            Paragraph("<b>Submitted by:</b><br/>Arshpreet Singh&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;23103341&nbsp;&nbsp;B12<br/>Manjunath Rachakonda&nbsp;&nbsp;23103344&nbsp;&nbsp;B12", styles["CoverText"]),
        ],
    ], [2.65 * inch, 4.4 * inch], header=False, font_size=12))
    story.append(PageBreak())

    story.append(para("Table of Contents", "H1"))
    toc = [
        "1. Introduction and Problem Statement",
        "2. Software Requirements Specification",
        "3. Software Design and UML Diagrams",
        "4. Implementation",
        "5. Code Optimization and Refactoring",
        "6. Software Testing",
        "7. Conclusion and Future Scope",
        "8. References",
    ]
    story.extend(bullets(toc))
    story.append(PageBreak())

    story.append(para("1. Introduction and Problem Statement", "H1"))
    story.append(para(
        "EZEmployee AI is a web-based HR management and workforce analytics application. It helps an HR user manage employee data, monitor workforce indicators, generate reports, and use AI/ML techniques for performance prediction, attrition risk scoring, and employee clustering.",
    ))
    story.append(para("Problem Statement", "H2"))
    story.append(para(
        "Many small and medium organizations maintain employee data in scattered spreadsheets. This makes it difficult to search records, update details, compare departments, identify performance trends, and prepare reports quickly. Manual analysis also increases the chance of errors and delays in HR decision-making.",
    ))
    story.append(para(
        "EZEmployee AI solves this problem by providing a centralized Streamlit application where employee records, dashboards, reports, and AI analytics are available in one place.",
    ))
    story.append(para("Relevance to Software Engineering Principles", "H2"))
    story.extend(bullets([
        "<b>Modularity:</b> the code is divided into separate modules for data management, CRUD, dashboard, AI analytics, and reports.",
        "<b>Abstraction:</b> reusable functions hide storage and ML logic from the UI layer.",
        "<b>Maintainability:</b> focused modules make future changes easier.",
        "<b>Usability:</b> navigation, tabs, forms, tables, and charts support a simple workflow.",
        "<b>Reliability:</b> CSV persistence keeps employee data available across sessions.",
        "<b>Scalability:</b> the architecture can later be extended with authentication, database storage, and automated testing.",
    ]))

    story.append(para("Project Objectives", "H2"))
    story.extend(bullets([
        "Provide add, view, search, update, delete, import, and export operations for employee records.",
        "Display dashboard metrics such as total employees, average salary, attendance, and high performers.",
        "Generate salary, performance, department, and HR summary reports.",
        "Predict employee performance using Random Forest classification.",
        "Calculate attrition risk using transparent rule-based scoring.",
        "Cluster employees using K-Means to identify similar workforce groups.",
    ]))
    story.append(PageBreak())

    story.append(para("2. Software Requirements Specification (SRS)", "H1"))
    story.append(para("2.1 Purpose", "H2"))
    story.append(para(
        "The purpose of this SRS is to define the functional and non-functional requirements of EZEmployee AI so that developers, testers, faculty evaluators, and users can understand the expected behavior of the system.",
    ))
    story.append(para("2.2 Scope", "H2"))
    story.append(para(
        "The system covers employee data management, visual HR dashboards, AI analytics, reports, and CSV import/export. It runs locally using Streamlit and uses a CSV file as persistent storage.",
    ))
    story.append(para("2.3 Functional Requirements", "H2"))
    story.append(table([
        ["ID", "Requirement"],
        ["FR-01", "The system shall load employee data from a CSV file."],
        ["FR-02", "The system shall create sample employee data if no CSV file exists."],
        ["FR-03", "The system shall allow the user to search and filter employees."],
        ["FR-04", "The system shall allow adding a new employee with required fields."],
        ["FR-05", "The system shall reject duplicate employee email addresses."],
        ["FR-06", "The system shall allow updating employee details."],
        ["FR-07", "The system shall allow deleting an employee after confirmation."],
        ["FR-08", "The system shall display dashboard charts and KPI cards."],
        ["FR-09", "The system shall predict employee performance using ML."],
        ["FR-10", "The system shall compute attrition risk scores."],
        ["FR-11", "The system shall cluster employees using K-Means."],
        ["FR-12", "The system shall generate HR, salary, and performance reports."],
        ["FR-13", "The system shall import and export employee data as CSV."],
    ], [0.85 * inch, 6.2 * inch]))
    story.append(para("2.4 Non-Functional Requirements", "H2"))
    story.append(table([
        ["Type", "Requirement"],
        ["Usability", "The application should be easy to navigate using sidebar pages and tabs."],
        ["Performance", "Charts, filters, and reports should respond quickly for the project dataset."],
        ["Reliability", "Employee data should remain consistent after add, update, delete, import, and export actions."],
        ["Maintainability", "Code should be organized in modules with readable function names."],
        ["Portability", "The project should run on a standard machine with Python and required packages."],
        ["Security", "Important form inputs should be validated and duplicate emails should be prevented."],
    ], [1.5 * inch, 5.55 * inch]))
    story.append(para("2.5 User Classes", "H2"))
    story.extend(bullets([
        "<b>HR Administrator:</b> manages employee records, imports/exports CSV data, checks dashboard and reports.",
        "<b>Manager / Viewer:</b> reviews analytics, salary summaries, and performance information.",
        "<b>Project Evaluator:</b> tests whether the software satisfies SE requirements and expected workflows.",
    ]))
    story.append(para("2.6 Operating Environment", "H2"))
    story.extend(bullets([
        "Operating system: Windows or any OS supporting Python and Streamlit.",
        "Runtime: Python 3.x.",
        "Browser: Chrome, Edge, Firefox, or another modern browser.",
        "Storage: local CSV file located at data/employees.csv.",
    ]))
    story.append(PageBreak())

    story.append(para("3. Software Design and UML Diagrams", "H1"))
    story.append(para(
        "The application uses a modular architecture. app.py is the entry point and page router. data_manager.py handles persistence. employee_crud.py handles employee operations. dashboard.py displays analytics. ai_engine.py performs ML-related processing. reports.py generates report views and exports.",
    ))

    use_case = r"""
                 +---------------------------------------------+
                 |               EZEmployee AI                 |
                 |---------------------------------------------|
HR User -------->| View Dashboard                              |
HR User -------->| Add / Search / Update / Delete Employee     |
HR User -------->| Import / Export CSV                         |
HR User -------->| Run Performance Prediction                  |
HR User -------->| View Attrition Risk                         |
HR User -------->| Cluster Employees                           |
HR User -------->| Generate HR / Salary / Performance Reports  |
                 +---------------------------------------------+
"""
    story.extend(diagram("3.1 Use Case Diagram", use_case))

    activity = r"""
[Start]
   |
   v
[Open Streamlit App]
   |
   v
[Load employees.csv or create sample data]
   |
   v
[Select Sidebar Page]
   |--------------------|------------------|----------------|
   v                    v                  v                v
[Dashboard]       [Employees CRUD]   [AI Analytics]     [Reports]
   |                    |                  |                |
   v                    v                  v                v
[View Charts]   [Save CSV Changes]  [Predict/Risk/Cluster] [Export CSV]
   |                    |                  |                |
   +--------------------+------------------+----------------+
                            |
                            v
                         [End]
"""
    story.extend(diagram("3.2 Activity Diagram", activity))

    class_diagram = r"""
+------------------+       +---------------------+
|      app.py      |------>|   data_manager.py   |
| set_page_config  |       | load_data()         |
| render_sidebar() |       | save_data()         |
| main()           |       | add/update/delete() |
+--------+---------+       | import/export_csv() |
         |                 +----------+----------+
         |                            ^
         v                            |
+------------------+       +---------+----------+
| employee_crud.py |------>|  employees.csv     |
| _view_search()   |       +--------------------+
| _add_employee()  |
| _update_employee()|
| _delete_employee()|
+------------------+
         |
         +----> dashboard.py: KPI cards, charts, department analytics
         +----> ai_engine.py: RandomForest, attrition rules, K-Means
         +----> reports.py: HR summary, salary analysis, exports
"""
    story.extend(diagram("3.3 Class / Module Diagram", class_diagram))

    sequence = r"""
User        app.py        data_manager        employee_crud        employees.csv
 |            |                |                    |                    |
 | Open app   |                |                    |                    |
 |----------->| load_data()    |                    |                    |
 |            |--------------->| read CSV           |------------------->|
 |            |<---------------| dataframe          |<-------------------|
 | Select Employees page       |                    |                    |
 |----------->| render(df)     |------------------->|                    |
 | Add record |                | add_employee()     |                    |
 |----------->|                |<-------------------|                    |
 |            |                | save_data()        |------------------->|
 |            | rerun UI       |                    |                    |
"""
    story.extend(diagram("3.4 Sequence Diagram: Add Employee", sequence))

    state = r"""
                 +-------------+
                 | App Started |
                 +------+------+
                        |
                        v
                 +-------------+
                 | Data Loaded |
                 +------+------+
                        |
      +-----------------+------------------+
      v                 v                  v
+-----------+   +---------------+   +--------------+
| Dashboard |   | Employee CRUD |   | AI Analytics |
+-----+-----+   +-------+-------+   +------+-------+
      |                 |                  |
      v                 v                  v
+-----------+   +---------------+   +--------------+
| Reports   |<--| CSV Updated   |-->| Model Output |
+-----------+   +---------------+   +--------------+
"""
    story.extend(diagram("3.5 State Diagram", state))

    deploy = r"""
+----------------------+
| User Browser         |
| Streamlit UI         |
+----------+-----------+
           |
           | HTTP localhost
           v
+----------------------+
| Local Python Runtime |
| app.py + modules     |
+----------+-----------+
           |
           v
+----------------------+
| Local File Storage   |
| data/employees.csv   |
+----------------------+
"""
    story.extend(diagram("3.6 Deployment Diagram", deploy))
    story.append(PageBreak())

    story.append(para("4. Implementation", "H1"))
    story.append(para("4.1 Technologies Used", "H2"))
    story.append(table([
        ["Technology", "Purpose"],
        ["Python", "Main programming language for logic and data processing."],
        ["Streamlit", "Frontend web application framework."],
        ["Pandas", "Dataframe operations, filtering, grouping, CSV import/export."],
        ["NumPy", "Numerical support used with ML/data operations."],
        ["Plotly", "Interactive charts in dashboard, AI analytics, and reports."],
        ["scikit-learn", "Random Forest classifier, K-Means clustering, train-test split, feature scaling."],
        ["CSV", "Local persistent storage for employee records."],
    ], [1.35 * inch, 5.7 * inch]))
    story.append(para("4.2 Code Structure and Key Modules", "H2"))
    story.append(table([
        ["File / Module", "Description"],
        ["app.py", "Application entry point. Defines page configuration, global CSS, sidebar navigation, and routes pages."],
        ["modules/data_manager.py", "Loads, saves, creates sample data, validates imported CSV files, and provides CRUD persistence helpers."],
        ["modules/employee_crud.py", "Contains screens for viewing, searching, adding, updating, deleting, importing, and exporting employees."],
        ["modules/dashboard.py", "Displays workforce KPIs, department distribution, salary charts, performance distribution, and training/attendance charts."],
        ["modules/ai_engine.py", "Implements performance prediction, attrition risk scoring, and employee clustering."],
        ["modules/reports.py", "Builds HR summary, salary analysis, performance report, and export screens."],
        ["data/employees.csv", "Stores employee records used by the whole application."],
    ], [1.75 * inch, 5.3 * inch]))
    story.append(para("4.3 Implementation Highlights", "H2"))
    story.extend(bullets([
        "Employee IDs are generated using the current maximum ID plus one.",
        "Required employee fields are validated before insertion.",
        "Duplicate email addresses are blocked during add operation.",
        "Dashboard charts are generated from live dataframe values.",
        "Random Forest predicts performance level from age, experience, salary, attendance, training hours, and completed projects.",
        "Attrition risk combines attendance, salary, performance, training, and experience into a score from 0 to 100.",
        "K-Means groups employees after scaling feature values with StandardScaler.",
    ]))
    story.append(PageBreak())

    story.append(para("5. Code Optimization and Refactoring", "H1"))
    story.append(para("Applied Coding Standards and Guidelines", "H2"))
    story.extend(bullets([
        "Used meaningful function names such as load_data, save_data, add_employee, update_employee, and export_csv.",
        "Separated business logic from presentation where practical.",
        "Placed repeated chart layout settings in helper functions.",
        "Used Pandas dataframe operations instead of manual row-by-row processing for filtering and grouping.",
        "Kept ML feature names in a shared FEATURES list inside ai_engine.py.",
        "Used Streamlit forms to group related input fields and avoid partial submission problems.",
    ]))
    story.append(para("Refactoring Examples", "H2"))
    story.append(table([
        ["Before Refactoring Idea", "After Refactoring in EZEmployee"],
        ["Saving CSV separately in every screen.", "Centralized save_data(df) in data_manager.py."],
        ["Repeated add/update/delete logic inside app.py.", "Employee operations moved to employee_crud.py."],
        ["Repeated Plotly styling in every chart.", "Dashboard and AI modules use helper layout functions."],
        ["Hard-coded ML columns in many places.", "ai_engine.py uses one FEATURES list for model input columns."],
    ], [2.6 * inch, 4.45 * inch]))
    story.append(para("Optimization Techniques Used", "H2"))
    story.extend(bullets([
        "Data is loaded once in app.py and passed to active modules.",
        "Numeric columns are converted immediately after loading to reduce later conversion errors.",
        "Grouping and aggregation are performed using Pandas built-in methods.",
        "ML models are trained only when the AI Analytics page is opened.",
        "CSV export uses in-memory byte data instead of temporary files.",
    ]))
    story.append(PageBreak())

    story.append(para("6. Software Testing", "H1"))
    story.append(para("6.1 Black Box Testing", "H2"))
    story.append(table([
        ["Technique", "Application in EZEmployee"],
        ["Equivalence Class Testing", "Valid and invalid employee records are tested, such as valid email vs duplicate email and valid salary vs out-of-range salary."],
        ["Boundary Value Testing", "Minimum and maximum values are checked for age, salary, attendance score, training hours, years of experience, and projects completed."],
        ["Decision Table Testing", "Different input combinations are checked for add employee: missing name, missing email, duplicate email, and valid data."],
    ], [1.7 * inch, 5.35 * inch]))
    story.append(para("6.2 White Box Testing", "H2"))
    story.extend(bullets([
        "Path testing verifies success and failure branches in add_employee, update_employee, delete_employee, and import_csv.",
        "Data flow testing verifies that form input is saved to CSV and then appears in dashboard and reports.",
        "Condition testing verifies attrition risk scoring branches for low attendance, low salary, low training, low performance, and low experience.",
        "Loop testing verifies dataframe iteration used during attrition scoring.",
    ]))
    story.append(para("6.3 Levels of Testing", "H2"))
    story.append(table([
        ["Level", "Description"],
        ["Unit Testing", "Individual helper functions such as get_next_id, load_data, save_data, import_csv, and risk scoring are checked separately."],
        ["Integration Testing", "Employee CRUD changes are tested with dashboard, AI analytics, reports, and CSV persistence."],
        ["System Testing", "The complete workflow is tested from app start to employee management, AI analytics, reporting, and export."],
    ], [1.35 * inch, 5.7 * inch]))
    story.append(para("6.4 Test Cases with Expected and Actual Output", "H2"))
    story.append(table([
        ["TC ID", "Test Case", "Expected Output", "Actual Output"],
        ["TC-01", "Open application", "Dashboard loads after CSV data is read.", "Passed"],
        ["TC-02", "Search employee by name", "Matching employee rows are displayed.", "Passed"],
        ["TC-03", "Add employee with valid data", "New employee is saved with new ID.", "Passed"],
        ["TC-04", "Add employee with missing name/email", "Validation error is shown.", "Passed"],
        ["TC-05", "Add duplicate email", "Duplicate email is rejected.", "Passed"],
        ["TC-06", "Update employee salary", "CSV and table show updated salary.", "Passed"],
        ["TC-07", "Delete employee after confirmation", "Employee is removed from dataset.", "Passed"],
        ["TC-08", "Import valid CSV", "New employee rows are added.", "Passed"],
        ["TC-09", "Import CSV missing required columns", "Error message lists missing columns.", "Passed"],
        ["TC-10", "Run performance prediction", "Predicted level and confidence are shown.", "Passed"],
        ["TC-11", "Open attrition risk tab", "Risk table and charts are displayed.", "Passed"],
        ["TC-12", "Export filtered CSV", "Downloadable CSV is generated.", "Passed"],
    ], [0.65 * inch, 2.15 * inch, 2.35 * inch, 1.9 * inch], font_size=7.8))
    story.append(para("6.5 Bug Reports", "H2"))
    story.append(table([
        ["Bug", "Status"],
        ["Some UI labels and emoji symbols displayed with encoding artifacts in the source/output environment.", "Known cosmetic issue; does not block functional behavior."],
        ["Duplicate employee emails could create conflicting records if not checked.", "Handled in add employee validation."],
        ["Invalid CSV files may break import if required columns are missing.", "Handled by import_csv required-column validation."],
    ], [4.5 * inch, 2.55 * inch]))
    story.append(PageBreak())

    story.append(para("7. Conclusion and Future Scope", "H1"))
    story.append(para(
        "EZEmployee AI successfully demonstrates a Software Engineering project with a clear problem statement, defined requirements, modular software design, implementation details, optimization ideas, and testing coverage. It is a practical HR application that combines employee record management with dashboards, reporting, and machine-learning analytics.",
    ))
    story.append(para("Future Scope", "H2"))
    story.extend(bullets([
        "Replace CSV storage with SQLite, MySQL, or PostgreSQL.",
        "Add login, authentication, and role-based access control.",
        "Add automated unit tests using pytest.",
        "Add employee attendance history and leave management.",
        "Improve prediction accuracy using larger historical datasets.",
        "Generate downloadable PDF reports directly from inside the Streamlit app.",
    ]))
    story.append(para("8. References", "H1"))
    story.extend(bullets([
        "EZEmployee project source code: app.py, modules/data_manager.py, modules/employee_crud.py, modules/dashboard.py, modules/ai_engine.py, modules/reports.py, and data/employees.csv.",
        "Python Software Foundation, Python 3 Documentation, https://docs.python.org/3/.",
        "Streamlit, Streamlit Documentation, https://docs.streamlit.io/.",
        "pandas Development Team, pandas Documentation, https://pandas.pydata.org/docs/.",
        "scikit-learn Developers, scikit-learn User Guide, https://scikit-learn.org/stable/user_guide.html.",
        "Plotly Technologies Inc., Plotly Python Documentation, https://plotly.com/python/.",
        "ReportLab, ReportLab User Guide, https://docs.reportlab.com/reportlab/userguide/.",
        "IEEE Computer Society, IEEE Recommended Practice for Software Requirements Specifications, IEEE Std 830.",
        "Roger S. Pressman and Bruce R. Maxim, Software Engineering: A Practitioner's Approach, McGraw-Hill Education.",
    ]))

    doc.build(story, onFirstPage=page_number, onLaterPages=page_number)
    print(OUTPUT_FILE)


if __name__ == "__main__":
    build()
