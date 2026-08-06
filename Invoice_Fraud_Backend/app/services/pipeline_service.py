# from app.pipeline_DB.pipeline_runner import run_pipeline

# def execute_pipeline(document_id: int):

#     try:
#         print("Pipeline called")
#         print(document_id)
        
#         run_pipeline(document_id)  

#         print("Pipeline finished")

#         return {
#             "status": "success",
#             "document_id": document_id
#         }

#     except Exception as e:

#         return {
#             "status": "failed",
#             "message": str(e)
#         } 



# from app.pipeline_DB.pipeline_runner import run_pipeline
# import traceback


# def execute_pipeline(document_id: int):

#     try:
#         print("\n===================================")
#         print("Pipeline called from FastAPI")
#         print("===================================")
#         print(f"Document ID : {document_id}")

#         # Run complete pipeline
#         run_pipeline(document_id)

#         print("\n===================================")
#         print("Pipeline finished successfully")
#         print("===================================")

#         return {
#             "status": "success",
#             "document_id": document_id
#         }

#     except Exception as e:

#         print("\n===================================")
#         print("Pipeline execution failed")
#         print("===================================")

#         traceback.print_exc()

#         return {
#             "status": "failed",
#             "document_id": document_id,
#             "message": str(e)
#         }  



from app.pipeline_DB.pipeline_runner import run_pipeline
import traceback


def execute_pipeline(document_id: int, already_exists: bool):

    try:

        print("\n===================================")
        print("Pipeline called from FastAPI")
        print("===================================")
        print(f"Document ID    : {document_id}")
        print(f"Already Exists : {already_exists}")

        # Run complete pipeline
        run_pipeline(document_id, already_exists)

        print("\n===================================")
        print("Pipeline finished successfully")
        print("===================================")

        return {
            "status": "success",
            "document_id": document_id,
            "already_exists": already_exists
        }

    except Exception as e:

        print("\n===================================")
        print("Pipeline execution failed")
        print("===================================")

        traceback.print_exc()

        return {
            "status": "failed",
            "document_id": document_id,
            "already_exists": already_exists,
            "message": str(e)
        }