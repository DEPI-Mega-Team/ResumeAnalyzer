from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body, File
from fastapi import UploadFile  
from fastapi.responses import HTMLResponse
import io
import uvicorn
from resume_analyzer import init_parser

app = FastAPI()

parser = init_parser()


@app.post("/parse", description="Parse resume and return the extracted information")
async def parse(resume: UploadFile = File(...)):
    
    resume_content = await resume.read()
    resume_io = io.BytesIO(resume_content)
    resume_io.name = resume.filename
    
    result = parser.parse(resume_io)
    return {'result': result}

@app.get("/", description="Home route", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content="""
    <html>
        <head>
            <title>Hello world</title>
        </head>
        <body>
            <h1>Hello world</h1>
        </body>
    </html>
    """, status_code=200)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)