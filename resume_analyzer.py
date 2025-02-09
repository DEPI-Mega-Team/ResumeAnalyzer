from Modules.parser import ResumeParser

def init_parser() -> ResumeParser:
    return ResumeParser()

def parse_resume(parser: ResumeParser, resume: str) -> dict:
    return parser.parse(resume)
