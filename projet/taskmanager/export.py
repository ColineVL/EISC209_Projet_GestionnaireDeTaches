import os
import io
import csv
import json
import xml.etree.ElementTree as ET
import xlsxwriter as xlsx

def create_file(file_type, filename, queryset, fields, zipObj):
    """
    This function create a file to the specified format wich contained a table, write it in the zip object. We only want
    to modify the zip object so we destroy the created file at the end
    :param file_type: the type of the file to generate ('csv','xls','json','html' or 'yaml')
    :param filename: the name of the file to generate
    :param queryset: the table contained in the file
    :param resource: the resource assiated withe the queryset
    :param zipObj: the zip object in wich we want to write
    :return: nothing
    """

    if file_type == 'csv':
        queryset_to_csv(queryset, fields,filename)
    elif file_type == 'json':
        queryset_to_json(queryset, fields,filename)
    elif file_type == 'html':
        queryset_to_xml(queryset, fields,filename)
    elif file_type == 'xlsx':
        queryset_to_xls(queryset, fields, filename)


    zipObj.write(filename)
    os.remove(filename)

def queryset_to_csv(queryset, fields, filename):
    file = open(filename,'w')
    writer = csv.writer(file)
    writer.writerow([field for field in fields])
    for row in queryset:
        line = []
        for field in fields:
            if field == 'members':
                line.append([member.username for member in row.__getattribute__(field).all()])
            else:
                line.append(row.__getattribute__(field))
        writer.writerow(line)
    file.close()

def queryset_to_json(queryset, fields, filename):
    file = open(filename,"w")
    result = dict()
    for row in queryset:
        row_dict = dict()
        for field in fields:
            if field == 'members':
                row_dict[field]=[member.username for member in row.__getattribute__(field).all()]
            else:
                row_dict[field] = row.__getattribute__(field).__str__()
        result[row.id] = row_dict
    file.write(json.dumps(result))
    file.close()

def queryset_to_xml(queryset, fields, filename):
    file = open(filename,"wb")
    table = ET.Element('table')
    head = ET.SubElement(table,'tr')
    for field in fields:
        head_field = ET.SubElement(head,'th')
        head_field.text = field

    for row in queryset:
        table_row = ET.SubElement(table,'tr')
        for field in fields:
            item = ET.SubElement(table_row,'td')
            if field == 'members':
                item.text= [member.username for member in row.__getattribute__(field).all()].__str__()
            else:
                item.text = row.__getattribute__(field).__str__()

    file.write(ET.tostring(table))
    file.close()

def queryset_to_xls(queryset, fields, filename):
    file = xlsx.Workbook(filename)
    worksheet = file.add_worksheet()
    bold = file.add_format({'bold':True})
    count=0
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for field in fields:
        worksheet.write(alphabet[count]+(1).__str__(), field, bold)
        count +=1
    row_number=2
    for row in queryset:
        col_number = 0
        for field in fields:
            if field == 'members':
                worksheet.write(alphabet[col_number]+row_number.__str__(),[member.username for member in row.__getattribute__(field).all()].__str__())
            else:
                worksheet.write(alphabet[col_number]+row_number.__str__(), row.__getattribute__(field).__str__())
                col_number +=1
        row_number +=1

    file.close()