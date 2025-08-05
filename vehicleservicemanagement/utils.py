from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa


def html_to_pdf_directly(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def write_pdf(template_src, context_dict={}, filename="result"):
    filename = filename
    template = get_template(template_src)
    html  = template.render(context_dict)

    result = open(filename, 'wb') # Changed from file to filename
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    result.close()