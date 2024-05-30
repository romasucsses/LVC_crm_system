import os
from io import BytesIO
from celery import shared_task
from django.conf import settings
from django.template.loader import get_template
from weasyprint import HTML, CSS


@shared_task
def generate_invoice(context: dict):
    # Render HTML template with data
    template = get_template('my_pdf.html')
    html_content = template.render(context)

    # Determine the directory of the template
    template_dir = os.path.dirname(template.origin.name)
    css_path = os.path.join(template_dir, 'my_pdf_css.css')

    # Generate PDF
    pdf_file = BytesIO()
    html = HTML(string=html_content)
    if os.path.exists(css_path):
        css = CSS(filename=css_path)
        html.write_pdf(pdf_file, stylesheets=[css])
    else:
        html.write_pdf(pdf_file)

    # Save PDF to file
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'invoices', 'invoice.pdf')
    with open(pdf_path, 'wb') as output:
        output.write(pdf_file.getvalue())

    print(f"PDF generated at: {pdf_path}")


@shared_task()
def check_licence_status():
    pass
