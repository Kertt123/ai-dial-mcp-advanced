from typing import Any

from mcp_server.tools.users.base import BaseUserServiceTool


class SearchUsersTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "search_users"

    @property
    def description(self) -> str:
        return "Search users by optional attributes such as name, surname, email, or gender."

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Filter by first name"},
                "surname": {"type": "string", "description": "Filter by last name"},
                "email": {"type": "string", "description": "Filter by email address"},
                "gender": {"type": "string", "description": "Filter by gender"}
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> str:
        return await self._user_client.search_users(
            name=arguments.get("name"),
            surname=arguments.get("surname"),
            email=arguments.get("email"),
            gender=arguments.get("gender"),
        )
