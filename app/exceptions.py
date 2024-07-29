from fastapi import HTTPException, status

class ErrorHandler:
    @staticmethod
    def not_found(entity: str):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity} not found"
        )

    @staticmethod
    def bad_request(detail: str):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

    @staticmethod
    def internal_error(detail: str = "Internal server error"):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )
