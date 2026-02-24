import xml.etree.ElementTree as ET

root = ET.Element("records")
root.set("xmlns:dc", "http://purl.org/dc/elements/1.1/")

with open("decoded_links.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    parts = [p.strip() for p in line.split("|")]

    if len(parts) != 3:
        continue

    url, fond, filename = parts

    record = ET.SubElement(root, "record")

    ET.SubElement(record, "dc:title").text = filename
    ET.SubElement(record, "dc:creator").text = "Державний архів Тернопільської області"
    ET.SubElement(record, "dc:subject").text = fond
    ET.SubElement(record, "dc:identifier").text = url
    ET.SubElement(record, "dc:type").text = "Text"
    ET.SubElement(record, "dc:format").text = "application/pdf"
    ET.SubElement(record, "dc:source").text = "https://archives.te.gov.ua"

tree = ET.ElementTree(root)
ET.indent(tree, space="  ", level=0)
tree.write("dublin_core.xml", encoding="utf-8", xml_declaration=True)

print("Dublin Core файл створено успішно")
