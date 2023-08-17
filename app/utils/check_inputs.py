from fastapi import File, UploadFile
from fastapi import HTTPException


ALLOWED_EXTENSIONS = [".pdf"]
MAX_FILES = 1


async def check_inputs(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="Files must be provided.")
    if not any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Files must be pdf files "
                                                    f"Allowed Extensions: {ALLOWED_EXTENSIONS}")

    if len([file]) > MAX_FILES:
        raise HTTPException(status_code=400, detail=f"Maximum of {MAX_FILES} files allowed.")
