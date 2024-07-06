class CustomError:
    """
    Class with all error codes of the system.
    Error tuple: (<dev error msg>, <user error msg>)

    Dictionary: { <error code>: <error tuple> }

    Error return pattern:
        return Response({"error_code": <error_code>, "dev_error": <dev_error_msg>, "user_error": <user_error_msg>}, HTTP_400_BAD_REQUEST):

    """
    # TODO: Update all error messages on the entire code to use the same return pattern and error codes.
    error_dictionary = {
        "GE-0": ("Exception Raised:", "Something went wrong, please try again later or contact support."),
        "TC-0": ("Tool Category not found. Exception raised:", "Category not found."),
        "TC-1": ("No tools was found for this category. Exception raised:", "No tools found for this category."),
        "TC-2": ("Missing category parameter. Exception raised:", "Missing category on request."),
        "TM-0": ("Model not found. Exception raised:", "No model was found for this id."),
        "TM-1": ("Failed to update ToolsModel. Exception raised:", "Failed to update ToolsModel."),
        "TM-2": ("Missing category name parameter. Exception raised:", "Missing category name on request."),

    }

    @staticmethod
    def get_error_by_code(error_code, exception=None):
        exception = exception if exception else ''
        return {"error_code": error_code,
                "dev_error": f"{CustomError.error_dictionary[error_code][0]} {exception}",
                "user_error": CustomError.error_dictionary[error_code][1]
                }
