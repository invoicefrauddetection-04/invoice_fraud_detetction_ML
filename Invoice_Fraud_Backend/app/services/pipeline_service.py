from app.pipeline_DB.pipeline_runner import run_pipeline

def execute_pipeline(document_id: int):

    try:

        run_pipeline(document_id)

        return {
            "status": "success",
            "document_id": document_id
        }

    except Exception as e:

        return {
            "status": "failed",
            "message": str(e)
        }