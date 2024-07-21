class CustomError:
    """
    Class with all error codes of the system.
    Error tuple: (<dev error msg>, <user error msg>)

    Dictionary: { <error code>: <error tuple> }

    Error return pattern:
        return Response({"error_code": <error_code>, "dev_error": <dev_error_msg>, "user_error": <user_error_msg>}, HTTP_400_BAD_REQUEST):

    """

    error_dictionary = {
        "GE-0": ("Exception Raised:", "Something went wrong, please try again later or contact support."),
        "TC-0": ("Tool Category not found. Exception raised:", "Category not found."),
        "TC-1": ("No tools were found for this category. Exception raised:", "No tools found for this category."),
        "TC-2": ("Missing category parameter. Exception raised:", "Missing category on request."),
        "TO-0": ("No tools were found!. Exception raised:", "No tools found."),
        "TO-1": ("No tools were found for this ID!. Exception raised:", "No tools found for the requested ID."),
        "T0-2": ("Error while serializing Tool. Exception raised:",
                 "Something went wrong, please try again later or contact support."),
        "TM-0": ("Model not found. Exception raised:", "No model was found for this id."),
        "TM-1": ("Failed to update ToolsModel. Exception raised:", "Failed to update ToolsModel."),
        "TM-2": ("Missing category name parameter. Exception raised:", "Missing category name on request."),
        "TM-3": ("No tools model were found!. Exception raised:", "No tools model found."),
        "TM-4": ("Error while serializing Tools Model. Exception raised:",
                 "Something went wrong, please try again later or contact support."),
        "TH-0": ("Error while serializing Tool History. Exception raised:",
                 "Something went wrong, please try again later or contact support."),
        "TH-1": (
            "No tools rental were found for this user. Exception raised:",
            "This user currently has no rental history."),
        "PRC-0": ("Error while serializing Rental Cart. Exception raised:",
                  "Something went wrong, please try again later or contact support."),
        "PRC-1": ("Same tools model with different rental_dates. Exception raised:",
                  "Same Tool Model can only be rented for the same amount of days."),
        "PRC-2": (
            "No rental cart was found for this user. Exception raised:", "No rental cart was found for this user."),
        "PRC-3": ("No items in user rental cart. Exception raised:", "User Cart is Empty."),
        "POC-0": (
            "Error while serializing Rental Order. Exception raised:", "Something went wrong, please try again later."),
        "POC-1": ("Rental Order Not Found. Exception raised:",
                  "Rental Order not found. Go back to the rental cart and try again."),
        "POC-2": ("Open Rental Order Not Found. Exception raised:",
                  "Open Rental Order not found. Go back to the rental cart and try again."),
        "UE-0": ("User not found. Exception raised:", "Email or Password are invalid."),
        "UE-1": ("Error while serializing User. Exception raised:", "Something went wrong, please try again later."),
        "UE-2": ("User not found. Exception raised:", "User not found."),
        "UE-3": ("Empty Password. Exception raised:", "Password must be passed in and cannot be null or empty."),
        "UE-4": ("Manager Group Not Found. Exception raised:", "Manager group not found. Please contact support."),
        "UE-5": ("User is already a manager. Exception raised:", "User is already a manager."),
        "CB-0": ("Empty User Input. Exception raised:", "Empty Input."),
    }

    @staticmethod
    def get_error_by_code(error_code, exception=None):
        exception = exception if exception else ''
        return {"error_code": error_code,
                "dev_error": f"{CustomError.error_dictionary[error_code][0]} {exception}",
                "user_error": CustomError.error_dictionary[error_code][1]
                }
