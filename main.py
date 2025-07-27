from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import csv

app = FastAPI()
templates = Jinja2Templates(directory="templates")

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <h1>Deployed Successfully</h1>
    <p>Check your CSV output: <a href='/csv-table'>CSV Table</a></p>
    """


@app.get("/csv-table", response_class=HTMLResponse)
def show_table(request: Request):
    file_path = "Table_Input.csv"
    table_data = []
    value_map = {}

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  

            for row in reader:
                if len(row) >= 2:
                    key, val = row[0], int(row[1])
                    table_data.append((key, val))
                    value_map[key] = val

        alpha = value_map.get("A5", 0) + value_map.get("A20", 0)
        beta = value_map.get("A15", 0) // value_map.get("A7", 1)
        charlie = value_map.get("A13", 0) * value_map.get("A12", 0)

        table2 = {
            "Alpha": alpha,
            "Beta": beta,
            "Charlie": charlie
        }

    except FileNotFoundError:
        return templates.TemplateResponse("tableoutput.html", {
            "request": request,
            "error": "CSV not found.",
            "table_data": [],
            "table2": None
        })

    return templates.TemplateResponse("tableoutput.html", {
        "request": request,
        "table_data": table_data,
        "table2": table2
    })

@app.get("/download")
def download_csv():
    return FileResponse("Table_Input.csv", filename="Table_Input.csv", media_type="text/csv")
