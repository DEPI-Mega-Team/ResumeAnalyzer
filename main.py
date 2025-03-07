from fastapi import FastAPI
from fastapi.params import File
from fastapi import UploadFile  
import io
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)