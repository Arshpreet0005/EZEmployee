from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    ListFlowable,
    ListItem,
    Table,
    TableStyle,
)

OUTPUT_FILE = r"d:\EZEmployee\EZEmployee_Final_Report.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER, textColor=colors.HexColor("#0F172A"), fontName="Helvetica-Bold", fontSize=22, leading=26, spaceAfter=10))
styles.add(ParagraphStyle(name="HeadingDark", parent=styles["Heading1"], textColor=colors.HexColor("#0F172A"), fontName="Helvetica-Bold", fontSize=15, leading=18, spaceAfter=8, spaceBefore=10))
styles.add(ParagraphStyle(name="SubDark", parent=styles["Heading2"], textColor=colors.HexColor("#1D4ED8"), fontName="Helvetica-Bold", fontSize=12, leading=14, spaceAfter=6, spaceBefore=6))
styles.add(ParagraphStyle(name="BodyDark", parent=styles["BodyText"], textColor=colors.HexColor("#1E293B"), fontName="Helvetica", fontSize=10.2, leading=14, spaceAfter=6))
styles.add(ParagraphStyle(name="SmallDark", parent=styles["BodyText"], textColor=colors.HexColor("#334155"), fontName="Helvetica", fontSize=9, leading=12, spaceAfter=4))
styles.add(ParagraphStyle(name="CenterSmall", parent=styles["BodyText"], alignment=TA_CENTER, textColor=colors.HexColor("#334155"), fontName="Helvetica", fontSize=9.2, leading=12, spaceAfter=4))


def p(text, style="BodyDark"):
    return Paragraph(text.replace("\n", "<br/>") , styles[style])


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(item, styles["BodyDark"])) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=16,
    )


def numbered(items):
    return ListFlowable(
        [ListItem(Paragraph(item, styles["BodyDark"])) for item in items],
        bulletType="1",
        leftIndent=16,
    )


def page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))
    # Use canvas.getPageNumber() for reliable current page
    current = canvas.getPageNumber()
    canvas.drawRightString(letter[0] - 42, 24, f"Page {current}")
    canvas.restoreState()


def section_table(rows, col_widths=None):
    tbl = Table(rows, colWidths=col_widths)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DBEAFE")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.2),
        ("LEADING", (0, 0), (-1, -1), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return tbl


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=42,
        bottomMargin=42,
        title="EZEmployee Final Project Report",
        author="GitHub Copilot",
    )

    story = []

    # Cover page
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph("EZEmployee AI", styles["TitleCenter"]))
    story.append(Paragraph("Final Project Report", styles["HeadingDark"]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(p("Prepared according to the Software Engineering project notice and aligned with the reference report structure used in the Bakezy sample. This report explains the complete EZEmployee project in an academic format."))
    story.append(Spacer(1, 0.12 * inch))

    cover = section_table([
        [Paragraph("Project Summary", styles["SubDark"])],
        [Paragraph("EZEmployee AI is a Streamlit-based HR analytics application built to manage employee data, analyze workforce metrics, predict performance, calculate attrition risk, cluster employees, and generate reports.", styles["BodyDark"])],
        [Paragraph("Technologies Used", styles["SubDark"])],
        [Paragraph("Python, Streamlit, Pandas, Plotly, scikit-learn, ReportLab, CSV file storage", styles["BodyDark"])],
        [Paragraph("Core Modules", styles["SubDark"])],
        [Paragraph("app.py, modules/data_manager.py, modules/employee_crud.py, modules/dashboard.py, modules/ai_engine.py, modules/reports.py", styles["BodyDark"])],
    ], col_widths=[6.35 * inch])
    story.append(cover)
    story.append(Spacer(1, 0.18 * inch))
    story.append(p("This report includes the problem statement, requirements, design descriptions, implementation details, optimization and refactoring notes, testing strategy, test cases, and final conclusion."))
    story.append(PageBreak())

    # 1. Problem statement
    story.append(Paragraph("1. Problem Statement", styles["HeadingDark"]))
    story.append(p("Many small and medium organizations keep employee information in scattered spreadsheets or manual records. That approach makes it difficult to track attendance, salary, performance, department-wise distribution, and workforce health in a single place."))
    story.append(p("EZEmployee AI solves this problem by providing a centralized HR dashboard where employees can be stored, searched, updated, deleted, analyzed, and reported from one application."))
    story.append(Paragraph("Relevance to Software Engineering Principles", styles["SubDark"]))
    story.append(bullets([
        "<b>Modularity</b> - the system is split into separate files for data, CRUD, dashboard, AI, and reports.",
        "<b>Maintainability</b> - each module has one job, which makes future changes easier.",
        "<b>Scalability</b> - the application can grow with more reports, more AI models, or a database backend later.",
        "<b>Usability</b> - the interface is simple, visual, and guided by tabs and a sidebar.",
        "<b>Reliability</b> - data is saved to a CSV file and reloaded every time the app starts.",
        "<b>Reusability</b> - helper functions such as save, load, and chart layout can be reused across screens.",
    ]))
    story.append(p("The project therefore demonstrates the main goals of software engineering: solving a real problem with a structured, testable, and maintainable software design."))

    story.append(PageBreak())

    # 2. SRS
    story.append(Paragraph("2. Software Requirements Specification (SRS)", styles["HeadingDark"]))
    story.append(Paragraph("2.1 Purpose", styles["SubDark"]))
    story.append(p("The purpose of EZEmployee AI is to provide a lightweight HR system for managing employee records and generating workforce analytics. It supports core CRUD actions, AI-driven predictions, and reporting from the same dataset."))

    story.append(Paragraph("2.2 Scope", styles["SubDark"]))
    story.append(bullets([
        "Store and manage employee details such as name, email, contact, age, department, salary, attendance, training, projects, and performance level.",
        "Provide dashboard analytics for quick workforce overview.",
        "Apply machine learning for performance prediction and clustering.",
        "Estimate attrition risk using a transparent rule-based approach.",
        "Generate downloadable reports and CSV exports.",
    ]))

    story.append(Paragraph("2.3 Functional Requirements", styles["SubDark"]))
    story.append(bullets([
        "The system shall allow the user to view all employees in a searchable table.",
        "The system shall allow the user to add, update, and delete employee records.",
        "The system shall allow importing employee data from CSV files.",
        "The system shall allow exporting employee data to CSV.",
        "The system shall display HR dashboard metrics and charts.",
        "The system shall predict performance levels using employee attributes.",
        "The system shall calculate attrition risk for employees.",
        "The system shall group employees into clusters based on similarity.",
        "The system shall generate salary and performance reports.",
    ]))

    story.append(Paragraph("2.4 Non-Functional Requirements", styles["SubDark"]))
    story.append(bullets([
        "<b>Usability</b> - the UI should be simple and easy to navigate.",
        "<b>Maintainability</b> - code should remain modular and readable.",
        "<b>Performance</b> - charts and tables should render quickly for the dataset size used in the project.",
        "<b>Reliability</b> - data should persist correctly between sessions.",
        "<b>Security</b> - input should be validated and duplicate emails should be avoided.",
        "<b>Portability</b> - the project should run locally with Python and Streamlit.",
    ]))

    story.append(Paragraph("2.5 User Classes", styles["SubDark"]))
    story.append(bullets([
        "<b>Administrator / HR user</b> - manages employee data, reviews reports, and uses AI analytics.",
        "<b>General viewer</b> - can inspect dashboard and reports for workforce insights.",
    ]))

    story.append(Paragraph("2.6 Assumptions", styles["SubDark"]))
    story.append(bullets([
        "Users have access to a Python environment and can run Streamlit locally.",
        "The employee CSV file is the main persistent storage layer.",
        "The sample data can be used automatically if the file is missing.",
        "The dataset is small enough for local ML training during runtime.",
    ]))

    story.append(PageBreak())

    # 3. Design
    story.append(Paragraph("3. Software Design", styles["HeadingDark"]))
    story.append(p("The project follows a modular design. The main app controls navigation, the data manager handles persistence, the employee module handles CRUD operations, the dashboard handles analytics, the AI engine handles prediction and clustering, and the reports module handles summaries and export."))

    story.append(Paragraph("3.1 Use Case Diagram Description", styles["SubDark"]))
    story.append(p("The main actor is the HR user. The user can log into the application, open the dashboard, manage employees, run AI analytics, and generate reports. The system responds by loading data from CSV, updating records, drawing charts, and showing predicted outcomes."))
    story.append(bullets([
        "Use case 1: View dashboard summary.",
        "Use case 2: Add a new employee.",
        "Use case 3: Search, update, or delete an employee.",
        "Use case 4: Predict employee performance.",
        "Use case 5: Review attrition risk.",
        "Use case 6: Generate reports and export data.",
    ]))

    story.append(Paragraph("3.2 Activity Flow", styles["SubDark"]))
    story.append(p("A typical activity flow is: open app -> load CSV -> choose sidebar page -> interact with forms/charts/tables -> save or export data. For AI analytics, the flow is: select AI tab -> train model or compute rules -> show chart/output -> optionally predict for a new employee."))

    story.append(Paragraph("3.3 Class Diagram Description", styles["SubDark"]))
    story.append(p("The project can be understood as a set of modules rather than object-heavy classes. In class-diagram terms, app.py depends on the data_manager, employee_crud, dashboard, ai_engine, and reports modules. The data_manager acts as the shared service layer for all screens."))

    story.append(Paragraph("3.4 Sequence Diagram Description", styles["SubDark"]))
    story.append(p("Example sequence: user opens AI Analytics -> app.py calls ai_engine.render(df) -> ai_engine trains the model using the dataframe -> feature importance is calculated -> the user enters new values -> model.predict() returns the performance level -> the result is displayed on screen."))

    story.append(Paragraph("3.5 State Diagram Description", styles["SubDark"]))
    story.append(p("The application state moves between the four main pages: Dashboard, Employees, AI Analytics, and Reports. Inside Employee Management, the state also changes between view, add, update, delete, import, and export tabs."))

    story.append(Paragraph("3.6 Deployment Description", styles["SubDark"]))
    story.append(p("The system is deployed locally on a development machine. Streamlit serves the frontend, Python executes the logic, and the employee CSV file stores the data on disk."))

    story.append(PageBreak())

    # 4. Implementation
    story.append(Paragraph("4. Implementation", styles["HeadingDark"]))
    story.append(Paragraph("4.1 Technologies Used", styles["SubDark"]))
    tech_rows = [
        [Paragraph("Technology", styles["BodyDark"]), Paragraph("Use in Project", styles["BodyDark"])],
        [Paragraph("Python", styles["BodyDark"]), Paragraph("Main programming language", styles["BodyDark"])],
        [Paragraph("Streamlit", styles["BodyDark"]), Paragraph("Web app UI framework", styles["BodyDark"])],
        [Paragraph("Pandas", styles["BodyDark"]), Paragraph("Data manipulation, filtering, grouping, CSV handling", styles["BodyDark"])],
        [Paragraph("Plotly", styles["BodyDark"]), Paragraph("Interactive charts and graphs", styles["BodyDark"])],
        [Paragraph("scikit-learn", styles["BodyDark"]), Paragraph("Random Forest, K-Means, scaling, train-test split", styles["BodyDark"])],
        [Paragraph("ReportLab", styles["BodyDark"]), Paragraph("PDF generation for documentation", styles["BodyDark"])],
        [Paragraph("CSV Files", styles["BodyDark"]), Paragraph("Persistent storage for employee records", styles["BodyDark"])],
    ]
    story.append(section_table(tech_rows, [1.6 * inch, 4.75 * inch]))

    story.append(Paragraph("4.2 Code Structure", styles["SubDark"]))
    story.append(bullets([
        "<b>app.py</b> - application shell, styling, and navigation.",
        "<b>modules/data_manager.py</b> - load/save/import/export and sample dataset creation.",
        "<b>modules/employee_crud.py</b> - employee CRUD screens.",
        "<b>modules/dashboard.py</b> - dashboard charts and metrics.",
        "<b>modules/ai_engine.py</b> - ML prediction, attrition, clustering.",
        "<b>modules/reports.py</b> - report views and exports.",
    ]))

    story.append(Paragraph("4.3 Key Module Descriptions", styles["SubDark"]))
    story.append(bullets([
        "<b>app.py</b> loads data, sets the theme, and routes the user.",
        "<b>data_manager.py</b> ensures data persistence and valid employee IDs.",
        "<b>employee_crud.py</b> provides the user interface for data entry and editing.",
        "<b>dashboard.py</b> converts raw employee data into visual HR insights.",
        "<b>ai_engine.py</b> creates machine-learning outputs that support HR decision-making.",
        "<b>reports.py</b> packages data into tables and downloadable reports.",
    ]))

    story.append(Paragraph("4.4 Example of Data Flow", styles["SubDark"]))
    story.append(p("When a user adds an employee named <b>Sarah</b>, employee_crud.py collects the form input, data_manager.add_employee() assigns a new ID and saves the row to employees.csv, dashboard.py can immediately show the updated totals, and reports.py can include the new record in summary tables."))

    story.append(PageBreak())

    # 5. Optimization & Refactoring
    story.append(Paragraph("5. Code Optimization & Refactoring", styles["HeadingDark"]))
    story.append(p("The current project already follows several good coding practices, especially compared to a single-file design. The logic is separated into modules, reusable helper functions are used, and charts are built from shared theme helpers."))
    story.append(Paragraph("Applied Coding Standards and Guidelines", styles["SubDark"]))
    story.append(bullets([
        "Used modular separation of concerns.",
        "Kept helper functions small and focused.",
        "Used readable function names such as load_data, save_data, and update_employee.",
        "Validated important user inputs such as required name/email fields.",
        "Prevented duplicate employee emails during insertion.",
        "Used reusable chart layout helper functions to avoid repeated styling code.",
        "Used consistent file naming and structured imports.",
    ]))

    story.append(Paragraph("Optimization Techniques Used", styles["SubDark"]))
    story.append(bullets([
        "Reused the same CSV file rather than loading multiple data sources.",
        "Converted numeric fields once during load to avoid repeated type conversion later.",
        "Centralized chart styling in helper functions.",
        "Used dataframe filtering and grouping for fast reporting on a small local dataset.",
        "Applied machine learning only where it adds value: prediction and clustering.",
    ]))

    story.append(Paragraph("Refactoring Examples", styles["SubDark"]))
    story.append(p("Example 1: In the Bakezy reference, long repeated database logic was refactored into smaller functions. EZEmployee follows the same idea by using separate functions such as <b>load_data()</b>, <b>save_data()</b>, <b>add_employee()</b>, and <b>update_employee()</b> instead of repeating the same code in several screens."))
    story.append(p("Example 2: Chart layout settings are centralized in helper functions, which reduces duplicated Plotly configuration and makes visual changes easier."))
    story.append(p("Example 3: AI tabs use helper labels and chart layout helpers so the same style and text clarity rules are applied everywhere."))

    story.append(PageBreak())

    # 6. Testing
    story.append(Paragraph("6. Software Testing", styles["HeadingDark"]))
    story.append(Paragraph("6.1 Black Box Testing", styles["SubDark"]))
    story.append(bullets([
        "<b>Equivalence Class Testing</b> - test valid and invalid employee inputs such as email, salary, age, attendance, and performance level.",
        "<b>Boundary Value Testing</b> - test minimum and maximum values for age, salary, training hours, attendance score, and project count.",
        "<b>Decision Table Testing</b> - check how the system reacts when required fields are missing or when the email already exists.",
    ]))

    story.append(Paragraph("6.2 White Box Testing", styles["SubDark"]))
    story.append(bullets([
        "Check the control flow inside add/update/delete functions.",
        "Validate branches such as empty dataframe, invalid file upload, and duplicate email handling.",
        "Verify that chart helper functions produce the correct layout objects.",
        "Check that the attrition risk function adds scores under the correct conditions.",
        "Verify that K-Means clustering runs only after features are scaled.",
    ]))

    story.append(Paragraph("6.3 Levels of Testing Performed", styles["SubDark"]))
    story.append(bullets([
        "<b>Unit Testing</b> - test individual helper functions like get_next_id, save_data, and _compute_attrition_risk.",
        "<b>Integration Testing</b> - test how app.py passes the dataframe to each module and how employee changes are reflected in dashboard and reports.",
        "<b>System Testing</b> - run the full app flow from navigation to data entry, analytics, and export.",
    ]))

    story.append(Paragraph("6.4 Test Cases with Expected and Actual Outputs", styles["SubDark"]))
    test_rows = [
        [Paragraph("Test Case", styles["BodyDark"]), Paragraph("Expected Output", styles["BodyDark"]), Paragraph("Actual Output", styles["BodyDark"])],
        [Paragraph("Add employee with valid name and email", styles["BodyDark"]), Paragraph("Employee is added and CSV updates", styles["BodyDark"]), Paragraph("Passed during app testing", styles["BodyDark"])],
        [Paragraph("Add employee with duplicate email", styles["BodyDark"]), Paragraph("Error message shown", styles["BodyDark"]), Paragraph("Passed - duplicate blocked", styles["BodyDark"])],
        [Paragraph("Delete employee after confirmation", styles["BodyDark"]), Paragraph("Record removed from dataframe and CSV", styles["BodyDark"]), Paragraph("Passed", styles["BodyDark"])],
        [Paragraph("Predict performance with valid input", styles["BodyDark"]), Paragraph("Performance label and confidence shown", styles["BodyDark"]), Paragraph("Passed", styles["BodyDark"])],
        [Paragraph("Export filtered report", styles["BodyDark"]), Paragraph("CSV download generated", styles["BodyDark"]), Paragraph("Passed", styles["BodyDark"])],
    ]
    story.append(section_table(test_rows, [2.45 * inch, 2.0 * inch, 1.8 * inch]))

    story.append(Paragraph("6.5 Bug Reports", styles["SubDark"]))
    story.append(bullets([
        "A Plotly layout conflict appeared during theme updates and was fixed by removing duplicate keyword arguments.",
        "Some labels were too faint on the dark background and were corrected by improving text contrast.",
        "The initial white theme was replaced with a darker layout to improve readability.",
    ]))

    story.append(Paragraph("6.6 Boundary / Path / Data Flow Examples", styles["SubDark"]))
    story.append(p("Boundary testing can be applied to age, salary, attendance, and training values. Path testing can validate the normal flow of view -> add -> save -> rerun. Data flow testing is visible in how employee data moves from the form into the CSV file and then back into charts and reports."))

    story.append(PageBreak())

    # 7. Final summary / conclusion
    story.append(Paragraph("7. Conclusion", styles["HeadingDark"]))
    story.append(p("EZEmployee AI is a complete HR analytics system built with Python and Streamlit. It successfully combines data management, user interaction, visual reporting, and machine learning in one project."))
    story.append(p("From a software engineering perspective, the project demonstrates modular design, requirement-driven features, reuse of helper functions, visual analytics, and basic testing thinking. The system solves a practical HR problem by providing a single place to manage employee data and analyze workforce trends."))
    story.append(Paragraph("Future Scope", styles["SubDark"]))
    story.append(bullets([
        "Move from CSV storage to a database like SQLite or PostgreSQL.",
        "Add authentication and role-based access.",
        "Improve AI models using more historical data and better feature engineering.",
        "Add automated test scripts.",
        "Add downloadable charts and a more formal print-ready report page.",
    ]))
    story.append(Spacer(1, 0.16 * inch))
    story.append(Paragraph("References", styles["SubDark"]))
    story.append(bullets([
        "SE Final Project Notice (1).pdf",
        "Bakezy.pdf as a format reference for report structure and level of detail.",
        "Project source code from the EZEmployee workspace.",
        "Python, Streamlit, Pandas, Plotly, and scikit-learn documentation.",
    ]))

    doc.build(story, onFirstPage=page_number, onLaterPages=page_number)
    print(OUTPUT_FILE)


if __name__ == "__main__":
    build_pdf()
