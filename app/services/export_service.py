from fpdf import FPDF
import csv
import io


def build_report_csv(report: dict) -> bytes:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Показатель", "Значение"])
    writer.writerow(["Проверок", report["total_checks"]])
    writer.writerow(["Инцидентов", report["total_incidents"]])
    writer.writerow(["Критических", report["critical_incidents"]])
    writer.writerow(["Предупреждений", report["warning_incidents"]])
    writer.writerow(["Проблемные объекты", ", ".join(report["top_problem_objects"])])
    return output.getvalue().encode("utf-8")


def build_report_pdf(report: dict, date_from: str, date_to: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Отчёт мониторинга", ln=True)
    pdf.cell(0, 10, f"Период: {date_from} — {date_to}", ln=True)
    pdf.ln(4)
    pdf.cell(0, 10, f"Проверок: {report['total_checks']}", ln=True)
    pdf.cell(0, 10, f"Инцидентов: {report['total_incidents']}", ln=True)
    pdf.cell(0, 10, f"Критических: {report['critical_incidents']}", ln=True)
    pdf.cell(0, 10, f"Предупреждений: {report['warning_incidents']}", ln=True)
    pdf.ln(4)
    pdf.multi_cell(0, 10, "Проблемные объекты: " + ", ".join(report["top_problem_objects"]))
    return pdf.output(dest="S").encode("latin1")
