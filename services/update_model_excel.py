from openpyxl import load_workbook

def update_model_excel(new_rows):
    workbook = load_workbook("./model/base_dataV1.0.xlsx" )
    target_sheet = workbook.get_sheet_by_name("Sheet2")

    for new_row in new_rows:
        target_sheet.append(new_row)

    workbook.save("./model/base_dataV1.0.xlsx")
    workbook.close()