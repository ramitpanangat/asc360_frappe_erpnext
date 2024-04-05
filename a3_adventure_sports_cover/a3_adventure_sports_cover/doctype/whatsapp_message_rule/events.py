from frappe import get_meta, whitelist
from re import findall

@whitelist()
def document_meta(document, message):
    field_list = []
    metas = get_meta(document).fields
    for meta in metas:
        if meta.fieldtype not in ["Section Break", "Column Break", "Table"]:
            if meta.hidden == 0:
                metaData = {
                    "fieldname" : meta.fieldname,
                    "label": meta.label
                }
                field_list.append(metaData)
            else:
                if meta.label == "Policy Number":
                    metaData = {
                    "fieldname" : meta.fieldname,
                    "label": meta.label
                    }
                    field_list.append(metaData)
                elif meta.fieldname == "name_of_customer":
                    metaData = {
                    "fieldname" : meta.fieldname,
                    "label": meta.label
                    }
                    field_list.append(metaData)
    parameters = findall(r"\{([A-Za-z0-9_]+)\}", message)
    return {"fields":field_list, "parameters": parameters}
