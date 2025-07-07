import asyncio
import sys
from dependency_injector.wiring import Provide, inject
from app.containers import Container
from app.services.user_service import UserService

@inject
async def list_users(service: UserService = Provide[Container.user_service]):
    users = await service.list_users()
    print(users)


async def main():
    container = Container()
    await container.init_resources()  # ✅ 꼭 async로!
    container.wire(modules=[__name__])  # ✅ wiring은 그 이후에

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
