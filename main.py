from fastapi import FastAPI, UploadFile
from fastapi.params import File
from fastapi.responses import JSONResponse
import io
from resume_analyzer import init_parser

app = FastAPI()

parser = init_parser()


@app.post("/parse", description="Parse resume and return the extracted information")
async def parse(resume: UploadFile = File(...)) -> JSONResponse:
    
    resume_content = await resume.read()
    resume_io = io.BytesIO(resume_content)
    resume_io.name = resume.filename
    
    extension = resume.filename.split('.')[-1]
    if extension not in ['pdf', 'docx']:
        return {'error': 'Invalid file format. Only PDF and DOCX files are supported.'}
    
    result = parser.parse(resume_io)
    return JSONResponse(result)


if __name__ == "__main__":
    import os
    from Modules import constants as cs
    import uvicorn

    os.chdir(cs.workspace_dir)
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)