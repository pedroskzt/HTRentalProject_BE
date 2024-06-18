from api.Models.tools_model import Tools


class ToolsHelper:

    @staticmethod
    def get_all_tools_objects():
        return Tools.objects.all()
