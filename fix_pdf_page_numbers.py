from io import BytesIO

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas


INPUT_FILE = r"D:\Downloads\EZEmployee_SE_Final_Report (1)_removed.pdf"
OUTPUT_FILE = r"D:\Downloads\EZEmployee_SE_Final_Report_numbered.pdf"


def make_number_overlay(width, height, page_number):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))

    # Cover the old bottom-centre page number and write the corrected one.
    c.setFillColorRGB(1, 1, 1)
    c.rect((width / 2) - 55, 17, 110, 28, fill=1, stroke=0)

    c.setFillColorRGB(0, 0, 0)
    c.setFont("Times-Roman", 10)
    c.drawCentredString(width / 2, 30, str(page_number))
    c.save()

    packet.seek(0)
    return PdfReader(packet).pages[0]


def main():
    reader = PdfReader(INPUT_FILE)
    writer = PdfWriter()

    for index, page in enumerate(reader.pages, start=1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        overlay = make_number_overlay(width, height, index)
        page.merge_page(overlay)
        writer.add_page(page)

    with open(OUTPUT_FILE, "wb") as handle:
        writer.write(handle)

    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
