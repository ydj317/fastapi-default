import asyncio
import sys
from dependency_injector.wiring import Provide, inject
from app.core.containers import Container
from app.core.settings import settings
from app.services.user_service import UserService

# python -m app.command list

@inject
async def list_users(service: UserService = Provide[Container.user_service]):
    users = await service.list_users()
    print(users)


async def main():
    container = Container()
    container.config.from_dict(settings.dict())
    await container.init_resources()
    container.wire(modules=[__name__])

    if len(sys.argv) < 2:
        print("Enter params!")
        return

    if sys.argv[1] == "list":
        await list_users()
    else:
        print(f"Unknown params: {sys.argv[1]}")

    await container.shutdown_resources()


if __name__ == "__main__":
    asyncio.run(main())
