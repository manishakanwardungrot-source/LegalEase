from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.ai_service import generate_legal_response
from backend.services.export_service import export_document

router = APIRouter()


class GenerateRequest(BaseModel):
    prompt: str


class ExportRequest(BaseModel):
    content: str
    filename: str
    file_format: str


@router.get("/test")
def test():
    return {
        "message": "LegalEase backend working!"
    }


@router.post("/generate")
def generate(request: GenerateRequest):
    try:
        result = generate_legal_response(request.prompt)

        return {
            "success": True,
            "response": result
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"AI generation failed: {str(error)}"
        )


@router.post("/export")
def export_file(request: ExportRequest):
    try:
        output_path = export_document(
            content=request.content,
            filename=request.filename,
            file_format=request.file_format
        )

        return {
            "success": True,
            "message": "Document exported successfully",
            "file": output_path
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Export failed: {str(error)}"
        )