from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable, ListItem, Table, TableStyle
from reportlab.pdfbase.pdfmetrics import stringWidth

OUTPUT_FILE = r"d:\EZEmployee\EZEmployee_Code_Explanation.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER, textColor=colors.HexColor("#0F172A"), fontName="Helvetica-Bold", fontSize=20, leading=24, spaceAfter=14))
styles.add(ParagraphStyle(name="HeadingDark", parent=styles["Heading1"], textColor=colors.HexColor("#0F172A"), fontName="Helvetica-Bold", fontSize=15, leading=18, spaceAfter=8, spaceBefore=10))
styles.add(ParagraphStyle(name="BodyDark", parent=styles["BodyText"], textColor=colors.HexColor("#1E293B"), fontName="Helvetica", fontSize=10.2, leading=13.5, spaceAfter=6))
styles.add(ParagraphStyle(name="SmallDark", parent=styles["BodyText"], textColor=colors.HexColor("#334155"), fontName="Helvetica", fontSize=9, leading=12, spaceAfter=4))
styles.add(ParagraphStyle(name="SubDark", parent=styles["Heading2"], textColor=colors.HexColor("#1D4ED8"), fontName="Helvetica-Bold", fontSize=12, leading=14, spaceAfter=6))


def p(text, style="BodyDark"):
    return Paragraph(text.replace("\n", "<br/>") , styles[style])


def bullet_list(items):
    return ListFlowable(
        [ListItem(Paragraph(item, styles["BodyDark"])) for item in items],
        bulletType="bullet",
        start="circle",
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


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=letter,
        rightMargin=42,
        leftMargin=42,
        topMargin=46,
        bottomMargin=42,
        title="EZEmployee AI Code Explanation",
        author="GitHub Copilot",
    )

    story = []
    # Cover page
    story.append(Spacer(1, 1.05 * inch))
    story.append(Paragraph("EZEmployee AI", styles["TitleCenter"]))
    story.append(Paragraph("Complete Code Explanation PDF", styles["HeadingDark"]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(p("This document explains the full project in detail, file by file, with the goal of helping you understand what every function, class, chart, and screen is doing."))
    story.append(p("It covers the application shell, data management, employee CRUD features, dashboard charts, AI analytics, and report/export screens."))
    story.append(Spacer(1, 0.15 * inch))
    cover_box = Table(
        [[Paragraph("What this PDF includes", styles["SubDark"])],
         [Paragraph("1. Overall project flow and architecture", styles["BodyDark"])],
         [Paragraph("2. app.py and how the app starts", styles["BodyDark"])],
         [Paragraph("3. data_manager.py and CSV handling", styles["BodyDark"])],
         [Paragraph("4. employee_crud.py and employee editing screens", styles["BodyDark"])],
         [Paragraph("5. dashboard.py and HR visual summaries", styles["BodyDark"])],
         [Paragraph("6. ai_engine.py and machine learning features", styles["BodyDark"])],
         [Paragraph("7. reports.py and export/report generation", styles["BodyDark"])],
         [Paragraph("8. libraries used, design choices, and examples", styles["BodyDark"])],
        ],
        colWidths=[6.3 * inch],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DBEAFE")),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )
    story.append(cover_box)
    story.append(Spacer(1, 0.22 * inch))
    story.append(p("You can use this PDF as study notes, interview prep, or a project walkthrough. Each section includes a plain-English explanation and small examples so the code is easier to remember."))
    story.append(PageBreak())

    story.append(Paragraph("1. Overall Project Flow", styles["HeadingDark"]))
    story.append(p("EZEmployee AI is a Streamlit application. When the app starts, <b>app.py</b> loads the employee data, shows the sidebar navigation, and sends the user to one of four screens: Dashboard, Employees, AI Analytics, or Reports. The rest of the files each handle one screen or one supporting layer."))
    story.append(p("Think of the project like a small HR system. The CSV file acts like a lightweight database, the Streamlit app acts like the front end, and the modules act like separate features inside the product."))

    story.append(Paragraph("1. Overall Project Flow", styles["HeadingDark"]))
    story.append(p("EZEmployee AI is a Streamlit application. When the app starts, <b>app.py</b> loads the employee data, shows the sidebar navigation, and sends the user to one of four screens: Dashboard, Employees, AI Analytics, or Reports. The rest of the files each handle one screen or one supporting layer."))
    story.append(p("Think of the project like a small HR system. The CSV file acts like a lightweight database, the Streamlit app acts like the front end, and the modules act like separate features inside the product."))
    story.append(bullet_list([
        "<b>data_manager.py</b> handles CSV storage, loading, saving, import, export, and ID management.",
        "<b>employee_crud.py</b> handles employee viewing, searching, adding, updating, deleting, and CSV import/export.",
        "<b>dashboard.py</b> shows summary metrics and charts for HR overview.",
        "<b>ai_engine.py</b> trains the AI models and renders performance prediction, attrition risk, and clustering.",
        "<b>reports.py</b> creates HR summary, salary analysis, performance reports, and export tools.",
    ]))
    story.append(p("Overall data flow example: the user adds a new employee in the Employee Management screen, data_manager.py saves it to employees.csv, dashboard.py immediately uses the updated dataframe to refresh charts, and ai_engine.py can use the new row during prediction or clustering."))

    story.append(PageBreak())

    story.append(Paragraph("2. app.py", styles["HeadingDark"]))
    story.append(p("This is the main entry point of the app. It configures Streamlit, injects the custom CSS theme, loads the modules, renders the sidebar, and decides which page to show based on the selected navigation item."))
    story.append(Paragraph("What the key parts do", styles["SubDark"]))
    story.append(bullet_list([
        "<b>st.set_page_config(...)</b> sets the browser tab title, icon, layout width, and sidebar state.",
        "The long CSS block changes the look of the whole app: dark gradient background, styled cards, custom buttons, tab styles, and readable text colors.",
        "<b>render_sidebar()</b> builds the left sidebar with the app name and the page navigation radio buttons.",
        "<b>main()</b> loads the data and routes to the selected module: dashboard, employee CRUD, AI analytics, or reports.",
    ]))
    story.append(Paragraph("Detailed explanation", styles["SubDark"]))
    story.append(bullet_list([
        "The page configuration is important because Streamlit uses it to control the app appearance before any screen is drawn.",
        "The CSS block is not just decoration. It also makes the labels, cards, tabs, and buttons easier to read against the dark background.",
        "The sidebar radio buttons act like a simple navigation menu. When the user clicks a choice, the selected module is rendered on the page.",
        "The if/elif block in <b>main()</b> works like a route selector. It checks the selected page and calls the correct module function.",
    ]))
    story.append(Paragraph("Example in practice", styles["SubDark"]))
    story.append(p("If the user selects <b>AI Analytics</b>, then app.py calls <b>ai_engine.render(df)</b>. The dataframe <b>df</b> is passed into the module so that every chart, prediction, and table uses the current employee data."))
    story.append(p("In short, this file is the controller. It does not contain business logic; it connects the screens together and gives the whole app its visual theme."))

    story.append(PageBreak())

    story.append(Paragraph("3. modules/data_manager.py", styles["HeadingDark"]))
    story.append(p("This file is the data layer. It stores employee records in <b>data/employees.csv</b>, ensures the file exists, creates sample data when needed, and provides helper functions for CRUD and import/export."))
    story.append(Paragraph("What the key parts do", styles["SubDark"]))
    story.append(bullet_list([
        "<b>DATA_FILE</b> points to the CSV file used as the app's database.",
        "<b>DEPARTMENTS</b> is a fixed list of valid department names used in forms and filters.",
        "<b>PERFORMANCE_LABELS</b> maps numeric performance values to readable labels.",
        "<b>load_data()</b> creates the data folder if needed, creates sample records if the CSV does not exist, then loads the employee table with numeric columns converted to numbers.",
        "<b>save_data(df)</b> writes the dataframe back to the CSV file.",
        "<b>get_next_id(df)</b> finds the next employee ID.",
        "<b>add_employee()</b>, <b>update_employee()</b>, and <b>delete_employee()</b> perform the core CRUD operations.",
        "<b>search_employees()</b> filters rows by text matching in a chosen field.",
        "<b>import_csv()</b> validates uploaded CSV files, assigns new IDs, merges data, and saves it.",
        "<b>export_csv()</b> converts the dataframe to downloadable CSV bytes.",
        "<b>_create_sample_data()</b> creates the starter employee dataset with 20 example employees.",
    ]))
    story.append(Paragraph("Detailed explanation", styles["SubDark"]))
    story.append(bullet_list([
        "<b>load_data()</b> is called at startup. If the CSV file is missing, it automatically creates sample data so the app never starts empty.",
        "The numeric conversion loop makes sure columns such as age, salary, and attendance_score behave like numbers instead of strings.",
        "<b>add_employee()</b> assigns a new unique ID before saving. This prevents ID collisions when new employees are added.",
        "<b>update_employee()</b> finds the matching row by employee ID, changes the selected fields, and writes the updated dataframe back to disk.",
        "<b>delete_employee()</b> removes the selected employee and then resets the row index so the table stays neat.",
        "<b>import_csv()</b> protects the app from broken uploads by checking required columns first. If the file is valid, it merges imported employees with the existing records.",
    ]))
    story.append(Paragraph("Example in practice", styles["SubDark"]))
    story.append(p("If a new employee named <b>Sarah</b> is added from the form, <b>add_employee()</b> gives her the next ID, appends her row to the dataframe, and saves the updated CSV. If later the CSV is downloaded, her record is included automatically."))
    story.append(p("This file is the foundation of the app because every screen depends on the data stored here."))

    story.append(PageBreak())

    story.append(Paragraph("4. modules/employee_crud.py", styles["HeadingDark"]))
    story.append(p("This module builds the Employee Management page. It lets the user search, filter, add, update, delete, import, and export employee records."))
    story.append(Paragraph("What the key parts do", styles["SubDark"]))
    story.append(bullet_list([
        "<b>render(df)</b> creates the page title and the tab layout for view/search, add, update, delete, and import/export.",
        "<b>_view_search()</b> shows a searchable/filterable table and formats salary and performance labels for easy reading.",
        "<b>_add_employee()</b> displays a form for creating a new employee and checks that name and email are present and that the email is unique.",
        "<b>_update_employee()</b> lets the user choose an employee and edit their details inside a form.",
        "<b>_delete_employee()</b> shows a confirmation checkbox before deleting a record.",
        "<b>_import_export()</b> handles CSV upload and CSV download.",
    ]))
    story.append(Paragraph("Detailed explanation", styles["SubDark"]))
    story.append(bullet_list([
        "The tabs organize the workflow into separate tasks so the page is not crowded.",
        "The search section uses both name and email so users can find people quickly using different kinds of input.",
        "The department and performance filters help narrow down the dataset when there are many employees.",
        "The add form uses validation rules. It checks required fields and prevents duplicate emails, which is important for keeping clean employee records.",
        "The update form pre-fills existing values so editing is faster and less error-prone.",
        "The delete flow adds a confirmation checkbox to avoid accidental deletion.",
        "The import/export section supports real workplace use where HR teams often move data between spreadsheets and the app.",
    ]))
    story.append(Paragraph("Example in practice", styles["SubDark"]))
    story.append(p("Suppose the HR user searches for <b>Alice</b>. The table filters to matching rows only. If they open the add form and enter a repeated email, the app stops the save and shows an error. If they choose a worker from the update dropdown, the form fills with the current values and lets them edit only what changed."))
    story.append(p("This module mainly deals with user input and table display. It passes the actual saving and loading work to data_manager.py."))

    story.append(PageBreak())

    story.append(Paragraph("5. modules/dashboard.py", styles["HeadingDark"]))
    story.append(p("This module builds the HR Dashboard page. It gives a quick company overview using cards and charts."))
    story.append(Paragraph("What the key parts do", styles["SubDark"]))
    story.append(bullet_list([
        "It calculates top-level metrics such as total employees, average salary, average attendance, and number of high performers.",
        "It shows four metric cards at the top for the key HR numbers.",
        "It draws an employee-by-department bar chart, a performance distribution donut chart, an average salary by department bar chart, and an experience-vs-salary scatter plot.",
        "It also shows a combined chart for training hours and attendance by department.",
        "The helper function <b>_dark_chart_layout()</b> keeps all charts visually consistent with the dark theme.",
    ]))
    story.append(Paragraph("Detailed explanation", styles["SubDark"]))
    story.append(bullet_list([
        "The page starts by summarizing the whole workforce in a few numbers so managers can understand the company at a glance.",
        "The department chart shows where employees are concentrated.",
        "The performance donut chart shows the balance between low, average, and high performers.",
        "The salary chart helps compare compensation across departments.",
        "The scatter plot shows whether experience tends to move with salary and whether the points cluster as expected.",
        "The combined training/attendance chart helps identify departments that may need more learning support or engagement support.",
    ]))
    story.append(Paragraph("Example in practice", styles["SubDark"]))
    story.append(p("If Engineering has the largest employee count and Management has the highest salary values, the dashboard makes those patterns visible immediately without needing to read the full table."))
    story.append(p("This page is meant for fast scanning. It answers questions like: How many employees do we have? Which departments are bigger? Which departments pay more?"))

    story.append(PageBreak())

    story.append(Paragraph("6. modules/ai_engine.py", styles["HeadingDark"]))
    story.append(p("This module is the AI part of the app. It has three main tasks: predict employee performance, estimate attrition risk, and group employees using clustering."))
    story.append(Paragraph("What the key parts do", styles["SubDark"]))
    story.append(bullet_list([
        "<b>FEATURES</b> defines the six columns used by the machine learning models: age, years_experience, salary, attendance_score, training_hours, and projects_completed.",
        "<b>_train_performance_model()</b> trains a Random Forest classifier to predict performance level from the employee data.",
        "<b>_compute_attrition_risk()</b> calculates a rule-based risk score from attendance, salary, performance, training, and experience.",
        "<b>_cluster_employees()</b> uses K-Means clustering to group similar employees after scaling the numeric features.",
        "<b>render(df)</b> creates the three AI tabs: Performance Predictor, Attrition Risk, and Employee Clustering.",
        "<b>_performance_tab()</b> shows model accuracy, feature importance, an input form for predicting a new employee, and batch predictions for all employees.",
        "<b>_attrition_tab()</b> shows risk counts, risk charts, high-risk alerts, and a full risk assessment table.",
        "<b>_clustering_tab()</b> shows cluster charts, cluster averages, per-cluster employee tables, and AI-generated insights.",
    ]))
    story.append(Paragraph("Detailed explanation", styles["SubDark"]))
    story.append(bullet_list([
        "The performance model is supervised learning. It learns from existing employee records where the performance level is already known.",
        "The feature importance chart explains which employee attributes affect predictions the most.",
        "The input form lets the user test a hypothetical employee and see the predicted performance result.",
        "The confidence breakdown shows how sure the model is for each class.",
        "The attrition risk score is rule-based because it should be easy for HR teams to understand. It increases when attendance is low, salary is low compared with peers, training is low, or performance is weak.",
        "The clustering section is unsupervised learning. It groups similar employees without using a target label.",
        "The cluster profiles and insight cards translate the raw machine learning output into business language.",
    ]))
    story.append(Paragraph("Example in practice", styles["SubDark"]))
    story.append(p("If a new employee has strong attendance, more projects, and higher experience, the performance model is more likely to predict a high level. If another employee has low attendance, low salary, and short training hours, the attrition risk score will be higher."))
    story.append(p("The AI code uses both machine learning and business rules. The performance predictor and clustering are data-driven, while the attrition score is intentionally rule-based so it stays simple and explainable."))

    story.append(PageBreak())

    story.append(Paragraph("7. modules/reports.py", styles["HeadingDark"]))
    story.append(p("This module builds reporting and export views. It focuses on summaries that are useful for management and HR review."))
    story.append(Paragraph("What the key parts do", styles["SubDark"]))
    story.append(bullet_list([
        "<b>render(df)</b> creates the Reports page and its four tabs.",
        "<b>_hr_summary()</b> calculates total employees, departments, average age, average experience, salary, and attendance, then shows a department breakdown table.",
        "<b>_salary_analysis()</b> uses box plots to compare salary distribution by department and by performance level.",
        "<b>_performance_report()</b> shows training-hours-vs-projects scatter plots, performance by department, and a top performers table.",
        "<b>_export_data()</b> lets the user download all employees or a department-filtered CSV and previews the export.",
    ]))
    story.append(Paragraph("Detailed explanation", styles["SubDark"]))
    story.append(bullet_list([
        "The HR summary combines several workforce statistics into one report so leadership can review the overall state of the company.",
        "The salary analysis helps identify wide gaps, outliers, and compensation patterns across departments and performance groups.",
        "The performance report shows whether more training correlates with more completed projects.",
        "The top performers table is useful for recognition, promotion review, and talent planning.",
        "The export tools let users take the data out of the app and into Excel or another reporting system.",
    ]))
    story.append(Paragraph("Example in practice", styles["SubDark"]))
    story.append(p("A manager can open the salary report to compare salary ranges across departments, then switch to the performance report to see which employees are producing the most projects. If they need a spreadsheet for a meeting, they can download the full CSV immediately."))
    story.append(p("This module is mostly about summarizing the data in a way that is easy to present or export."))

    story.append(PageBreak())

    story.append(Paragraph("8. Main Libraries Used", styles["HeadingDark"]))
    story.append(bullet_list([
        "<b>streamlit</b> builds the interactive web app UI.",
        "<b>pandas</b> handles tables, filtering, grouping, and CSV data processing.",
        "<b>plotly.express</b> and <b>plotly.graph_objects</b> create charts and graphs.",
        "<b>scikit-learn</b> provides Random Forest, K-Means, StandardScaler, train/test split, and accuracy scoring.",
        "<b>os</b> checks and creates folders/files on disk.",
        "<b>warnings</b> is used to suppress unnecessary warnings.",
        "<b>io</b> is used in the reports module for export handling.",
    ]))

    story.append(Paragraph("9. How the Features Work Together", styles["HeadingDark"]))
    story.append(bullet_list([
        "The Dashboard gives quick visual summaries.",
        "Employee Management changes the underlying CSV data.",
        "AI Analytics reads the same CSV data and applies machine learning or rules.",
        "Reports turns the data into presentation-ready summaries and exports.",
        "Because all screens share the same dataframe source, any change in Employee Management appears across the whole application.",
    ]))

    story.append(Paragraph("10. Small Examples of Code Behavior", styles["HeadingDark"]))
    story.append(bullet_list([
        "If the CSV file does not exist, <b>load_data()</b> creates it automatically using sample employees.",
        "If the user deletes an employee, the record disappears from the table and from future charts.",
        "If the user adds a new employee with a high attendance score and strong experience, AI Analytics can use that row right away.",
        "If a department has only a few employees, the charts still render because pandas grouping handles the small dataset.",
        "If the app is reopened later, the saved CSV persists the previous edits.",
    ]))

    story.append(Paragraph("11. Important Design Choices", styles["HeadingDark"]))
    story.append(bullet_list([
        "The app uses a CSV file instead of a database, which keeps it simple and easy to run locally.",
        "The sidebar navigation keeps the application split into clear sections.",
        "The dark theme and card styles improve contrast and make the UI look cleaner.",
        "The AI feature set uses only six numeric employee fields, which makes the models straightforward and explainable.",
        "Performance prediction uses supervised learning, attrition risk uses a rule-based score, and clustering uses unsupervised learning.",
    ]))

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("12. Final Summary", styles["HeadingDark"]))
    story.append(p("Overall, the project is a complete HR dashboard and analytics system built with Streamlit. The code is separated cleanly into files so each part has one job: data handling, employee management, dashboard charts, AI analytics, and reports. That separation makes the app easier to understand, maintain, and expand."))
    story.append(p("If you want, I can also create a second PDF that explains the code line by line in even simpler words, or add screenshots and architecture diagrams to make it easier to revise before an interview or presentation."))

    doc.build(story, onFirstPage=page_number, onLaterPages=page_number)
    print(OUTPUT_FILE)


if __name__ == "__main__":
    build_pdf()
