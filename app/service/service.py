import asyncio
from app.utils.ban import ban_ip, ban_ip_with_timeout, unban_ip
from app.service.nobetnode_grpc import NobetServiceBase
from app.service.nobetnode_pb2 import Result


class NobetService(NobetServiceBase):
    async def BanUser(self, stream):
        request = await stream.recv_message()

        asyncio.create_task(ban_ip_with_timeout(
            request.ip, request.banDuration))

        reply = Result(
            success=True, message=f"Ip {request.ip} banned for {request.banDuration} seconds!")
        await stream.send_message(reply)

    async def UnBanUser(self, stream):
        request = await stream.recv_message()

        await unban_ip(request.ip)

        reply = Result(success=True, message=f"Ip {request.ip} unbanned!")
        await stream.send_message(reply)
