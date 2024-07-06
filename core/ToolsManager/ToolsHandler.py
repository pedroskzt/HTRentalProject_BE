from rest_framework import status
from rest_framework.response import Response

from api.Models.tools_model_model import ToolsModel
from api.Serializers.serializers import (ToolsSerializer, ToolsModelSerializer, ToolsHistorySerializer,
                                         ToolsCategorySerializer)
from core.CustomErrors.CustomErrors import CustomError
from core.ToolsManager.ToolsHelper import ToolsHelper


class ToolsHandler:

    @staticmethod
    def handler_get_all_tools():
        try:
            # Get all tools.
            tools_objects = ToolsHelper.get_all_tools_objects()
            if tools_objects:
                # If tools were found, serialize it and return the data.
                tools_ser = ToolsSerializer(tools_objects, many=True)
                return Response(tools_ser.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'user_error': "Something went wrong, please try again later or contact support.",
                             "dev_error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'user_error': "No tools were found."}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_get_all_tools_models():
        try:
            # Get the tools models
            tools_models_objects = ToolsHelper.get_all_tools_models_objects()

            tools_models_objects = ToolsHelper.count_available_tools_by_model(tools_models_objects)
            tools_models_objects = ToolsHelper.get_related_tools_models(tools_models_objects)
            if tools_models_objects:
                # If tools where found, serialize and return the data.
                tools_models_ser = ToolsModelSerializer(tools_models_objects, many=True)
                return Response(tools_models_ser.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'user_error': "Something went wrong, please try again later or contact support.",
                             "dev_error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'user_error': "No tools were found."}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_get_tools_model_by_id(model_id):
        try:
            tools_model = ToolsHelper.get_model_by_id(model_id)
            if not tools_model.exists():
                return Response(CustomError.get_error_by_code("TM-0"), status=status.HTTP_400_BAD_REQUEST)

            tools_model = ToolsHelper.count_available_tools_by_model(tools_model)
            tools_model = ToolsHelper.get_related_tools_models(tools_model)

            tools_model_serializer = ToolsModelSerializer(tools_model, many=True)
            return Response(tools_model_serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(CustomError.get_error_by_code("GE-0", str(e)), status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_get_tool(tool_id):
        try:
            tool = ToolsHelper.get_tool_by_id(tool_id)
            tool_serialized = ToolsSerializer(tool)
            return Response(tool_serialized.data, status=status.HTTP_200_OK)

        except ToolsModel.DoesNotExist:
            return Response(f"No tool was found with ID {tool_id}", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'user_error': "Something went wrong, please try again later or contact support.",
                             "dev_error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_get_tools_by_category(category_id):
        try:

            if not category_id:
                return Response(CustomError.get_error_by_code("TC-2"), status=status.HTTP_400_BAD_REQUEST)

            category = ToolsHelper.get_tool_category_by_id(category_id)
            if not category.exists():
                return Response(CustomError.get_error_by_code("TC-0"), status=status.HTTP_400_BAD_REQUEST)
            category = category.first()

            tools = ToolsHelper.get_tools_models_by_category(category)
            if not tools.exists():
                return Response(CustomError.get_error_by_code("TC-1"), status=status.HTTP_400_BAD_REQUEST)

            tools = ToolsHelper.count_available_tools_by_model(tools)

            tools_serializer = ToolsModelSerializer(tools, many=True)
            return Response(tools_serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(CustomError.get_error_by_code("GE-0", str(e)), status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_get_tools_history_by_user(user):
        try:
            history_objects = ToolsHelper.get_tools_history_by_user(user)
            if history_objects:
                history_objects = ToolsHelper.get_related_tools_history(history_objects)
                history_serializer = ToolsHistorySerializer(history_objects, many=True)
                return Response(history_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'user_error': "No tool rental were found for this user.",
                                 "dev_error": "No tool rental were found for this user."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'user_error': "Something went wrong, please try again later or contact support.",
                             "dev_error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_get_all_categories():
        category_objects = ToolsHelper.get_all_categories()
        category_serializer = ToolsCategorySerializer(category_objects, many=True)
        return Response(category_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def handler_add_tool(request):
        try:
            tool_model = ToolsHelper.get_tool_model(request.get("model"), request.get("brand"))

            if not tool_model:  # tool model doesnt exist, create one
                tool_category = ToolsHelper.get_tool_category_by_id(request.get("category"))
                if tool_category.exists() is False:
                    return Response(CustomError.get_error_by_code("TC-0"), status=status.HTTP_400_BAD_REQUEST)
                tool_category = tool_category.first()

                new_tool_model = ToolsModelSerializer(data=request, context={"category": tool_category})
                if new_tool_model.is_valid():
                    tool_model = new_tool_model.save()

                else:
                    return Response({'user_error': "Tool model cannot be added to the database.",
                                     "dev_error": new_tool_model.errors},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                tool_model = tool_model.first()

            context = {"model": tool_model}
            new_tool = ToolsSerializer(data={}, context=context)
            if new_tool.is_valid():
                new_tool.save()

            else:
                return Response({'user_error': "Tool cannot be added to the database.",
                                 "dev_error": new_tool.errors},
                                status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            return Response({'user_error': "Something went wrong, please try again later or contact support.",
                             "dev_error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response("Tool was successfully added.", status=status.HTTP_201_CREATED)

    @staticmethod
    def handler_update_tool(tool_id, request):
        try:
            tool = ToolsHelper.get_tool_by_id(tool_id)
            if not tool:
                return Response({'user_error': "Tool cannot be updated because it doesn't exist.",
                                 "dev_error": "Tool not found"}, status=status.HTTP_400_BAD_REQUEST)

            tool_data = {
                "available": request.get("available")
            }
            context = {"model": tool.model}

            if request.get("brand") and request.get("model"):
                tool_model = ToolsHelper.get_tool_model(request.get("model"), request.get("brand"))
                if tool_model.exists() is False:  # tool model doesn't exist, create one
                    if request.get('category') is None:
                        return Response(CustomError.get_error_by_code("TC-2"), status.HTTP_400_BAD_REQUEST)

                    tool_category = ToolsHelper.get_tool_category_by_id(request.get('category'))
                    if tool_category.exists() is False:
                        return Response(CustomError.get_error_by_code("TC-0"), status.HTTP_400_BAD_REQUEST)
                    tool_category = tool_category.first()

                    new_tool_model = ToolsModelSerializer(data=request, context={'category': tool_category})
                    if new_tool_model.is_valid():
                        tool_model = new_tool_model.save()

                    else:
                        return Response({'user_error': "Tool model cannot be added to the database.",
                                         "dev_error": new_tool_model.errors},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    tool_model = tool_model.first()

                    if tool.model == tool_model:  # Update the tools model values
                        tool_model_serializer = ToolsModelSerializer(tool_model, data=request)
                        if tool_model_serializer.is_valid():
                            tool_model_serializer.save()
                        else:
                            return Response(CustomError.get_error_by_code("TM-1"), status.HTTP_400_BAD_REQUEST)
                context['model'] = tool_model

            tool_serializer = ToolsSerializer(tool, data=tool_data, context=context)
            if tool_serializer.is_valid():
                tool_serializer.save()
            else:
                return Response({'user_error': "Tool cannot be updated.",
                                 "dev_error": tool_serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            return Response({'user_error': "Something went wrong, please try again later or contact support.",
                             "dev_error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response("Tool was successfully updated.", status=status.HTTP_201_CREATED)
