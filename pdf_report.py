from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_pdf(patient):
    patient_id = patient["id"].values[0]
    filename = f"patient_{patient_id}_drstroke_report.pdf"

    c = canvas.Canvas(filename, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "DrStroke – Stroke Risk Report")

    c.setFont("Helvetica", 12)
    y = 760

    for col in patient.columns:
        c.drawString(50, y, f"{col}: {patient[col].values[0]}")
        y -= 20

        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 800

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 40, "Educational Use Only – Not Medical Advice")

    c.save()
    return filename
