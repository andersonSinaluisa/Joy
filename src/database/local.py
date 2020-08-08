import xml.etree.cElementTree as ET
#import xml.dom as xml

import src.functions.asistente as voz
import src as _
from os import path,stat

ruta = path.join(_.DIRNAME,'files/data.xml')
rutaf =ruta.replace('\\','/')

from xml.etree import ElementTree
from xml.parsers.expat.errors import messages
import pprint



def readData():
    with open(rutaf, 'rt') as f:
        print()
        if stat(rutaf).st_size != 0:
            tree = ElementTree.parse(f)
            for node in tree.iter():
                if node.text is not None:
                    return node.text












def xmlsession(id,user):

    session = ET.Element("session")
    doc = ET.SubElement(session, "data")

    _user=ET.SubElement(doc, "U", name="user")
    _user.text =user
    _id= ET.SubElement(doc,'UID',name='id')
    _id.text=id
    arbol = ET.ElementTree(session)
    arbol.write(rutaf)
    voz.hablar('Bienvenido')
