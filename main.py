from fastapi import FastAPI
from fastapi.params import Body, File

import io
import uvicorn
from resume_analyzer import init_parser

app = FastAPI()

parser = init_parser()


@app.post("/parse")
async def parse(resume = File(...)):
    resume_content = await resume.read()
    resume_io = io.BytesIO(resume_content)
    resume_io.name = resume.filename
    
    result = parser.parse(resume_io)
    return {'result': result}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)