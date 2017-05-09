# -*- coding: utf-8 -*-
# try something like

from subprocess import Popen, PIPE
import os
import uuid
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.graphics.barcode import code128
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.lib.units import mm, inch, cm
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame, Table, Spacer
from reportlab.platypus import SimpleDocTemplate, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import datetime

tmp_uuid = uuid.uuid4()
ruta = "%s.pdf"%tmp_uuid
c = canvas.Canvas(ruta, pagesize=letter)
c.setFont("Helvetica",7)
c.drawString(14 * mm, 252 * mm, "Separador")
c.line(0, 1 * cm, 8.5 , 1 * cm)
c.showPage()
c.save()
p1 = Popen(["lp","-dlpfacil","-o","media=Statement",ruta], stdout=PIPE)
p1.wait()
result = ( p1.communicate()[0] )
p1.stdout.close()
#os.remove(ruta)
print "impreso"
