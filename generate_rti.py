import io
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

BASE_PDF = "pdf_templates/rti_background.pdf"
FONT = "Times-Bold"
FONT_SIZE = 11

SHOW_GRID = False   # True only when adjusting positions


def draw_grid(can, width, height, step=50):
    can.setFont("Times-Roman", 6)
    for x in range(0, int(width), step):
        can.drawString(x + 2, height - 10, str(x))
        can.line(x, 0, x, height)
    for y in range(0, int(height), step):
        can.drawString(2, y + 2, str(y))
        can.line(0, y, width, y)


def place(can, w, h, x_pct, y_pct, text):
    x = w * (x_pct / 100)
    y = h * (y_pct / 100)
    can.drawString(x, y, text)


def generate_filled_rti(data, output_path):
    base_reader = PdfReader(BASE_PDF)
    base_page = base_reader.pages[0]

    width = float(base_page.mediabox.width)
    height = float(base_page.mediabox.height)

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    can.setFont(FONT, FONT_SIZE)

    if SHOW_GRID:
        draw_grid(can, width, height)

    # =========================
    # APPLICANT DETAILS
    # =========================
    place(can, width, height, 19, 74, data["applicant_name"])
    place(can, width, height, 33, 71.3, data["guardian_name"])
    place(can, width, height, 17, 68.5, data["address"])

    place(can, width, height, 39, 66, data["phone"])
    place(can, width, height, 14, 63.5, data["mobile"])

    # =========================
    # FEE DETAILS
    # =========================
    place(can, width, height, 41, 50.5, data["fee_amount"])
    place(can, width, height, 36, 48.4, data["payment_mode"])
    place(can, width, height, 44, 45.5, data["payment_date"])
    
    
    place(can, width, height, 13, 45.5, data["favoring"])

    # =========================
    # DOCUMENT DETAILS
    # =========================
    place(can, width, height, 20, 40.4, data["photocopy_amount"])
    place(can, width, height, 28, 40.4, data["num_pages"])

    place(can, width, height, 29, 35.4, data["cd_amount"])

    # =========================
    # BPL STATUS
    # =========================
    place(can, width, height, 58, 30, data["bpl_status"])
    place(can, width, height, 24, 25, data["bpl_certificate"])

    # =========================
    # SIGNATURE SECTION
    # =========================
    place(can, width, height, 72, 12, data["applicant_name"])
    place(can, width, height, 72, 7.7, data["date"])

    can.save()
    packet.seek(0)

    overlay_pdf = PdfReader(packet)
    overlay_page = overlay_pdf.pages[0]

    writer = PdfWriter()
    base_page.merge_page(overlay_page)
    writer.add_page(base_page)

    with open(output_path, "wb") as f:
        writer.write(f)
