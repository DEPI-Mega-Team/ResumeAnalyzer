from fastapi import FastAPI
from fastapi.params import Body
import uvicorn
from resume_analyzer import init_parser

app = FastAPI()

parser = init_parser()


@app.post("/parse")
async def parse(resume: str = Body(..., embed= True)):
    result = parser.parse(resume)
    return {'result': result}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)