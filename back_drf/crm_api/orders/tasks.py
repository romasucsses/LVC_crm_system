import os
from datetime import datetime
from io import BytesIO
# from weasyprint import HTML

from celery import shared_task
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa


@shared_task
def generate_invoice(context: dict):
    # Render HTML template with data
    template = get_template('pdf_invoice_template.html')
    html = template.render(context)

    # Determine the directory of the template
    # template_dir = os.path.dirname(template.origin.name)
    # print(f"Template directory: {template_dir}")
    #
    # # Path to the CSS file located in the same directory as the template
    # css_path = os.path.join(template_dir, 'my_pdf_css.css')
    # print(f"CSS file path: {css_path}")
    #
    # # Check if the CSS file exists
    # if not os.path.exists(css_path):
    #     print(f"CSS file does not exist: {css_path}")
    # else:
    #     print(f"CSS file exists: {css_path}")

    css = None
    # try:
    #     with open(css_path, "r") as css_file:
    #         css = css_file.read()
    #         print(f"CSS file read successfully")
    #         print(f"CSS file content: {css[:100]}...")
    # except Exception as e:
    #     print(f"Error reading CSS file: {e}")

    # Create PDF
    pdf = BytesIO()
    if css is not None:
        pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=pdf, default_css=css)
    else:
        pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=pdf)

    # Save PDF to file
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'invoices', 'invoice.pdf')
    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(pdf.getvalue())

    print(f"PDF generated at: {pdf_path}")

    # # Return PDF response
    # response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
    # response['Content-Disposition'] = 'filename=invoice.pdf'
    # return response

# @shared_task
# def generate_invoice(context: dict):
#     # Render HTML template with data
#     template = get_template('pdf_invoice_template.html')
#     html = template.render(context)
#
#     # Create PDF
#     pdf = BytesIO()
#     HTML(string=html).write_pdf(pdf)
#
#     pdf_path = os.path.join(settings.MEDIA_ROOT, 'invoices', 'invoice.pdf')
#     with open(pdf_path, 'wb') as pdf_file:
#         pdf_file.write(pdf.getvalue())