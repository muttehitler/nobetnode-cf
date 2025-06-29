import logging
import asyncio
import os
import sys
from grpclib.server import Server
from grpclib.health.service import Health
from grpclib.utils import graceful_exit
from app import config
from app.utils.ban import unban_all, verify_cloudflare
from app.service.service import NobetService
from app.utils.ssl import create_secure_context, generate_keypair

logger = logging.getLogger(__name__)


async def main():
    await verify_cloudflare()

    if config.UNBAN_ALL_IN_STARTUP:
        asyncio.create_task(unban_all())

    if config.INSECURE:
        ssl_context = None
    else:
        if not all(
            (os.path.isfile(config.SSL_CERT_FILE), os.path.isfile(config.SSL_KEY_FILE))
        ):
            logger.info("Generating a keypair for nobetnode.")
            generate_keypair(config.SSL_KEY_FILE, config.SSL_CERT_FILE)

        if not os.path.isfile(config.SSL_CLIENT_CERT_FILE):
            logger.error("No certificate provided for the client; exiting.")
            sys.exit(1)
        ssl_context = create_secure_context(
            config.SSL_CERT_FILE,
            config.SSL_KEY_FILE,
            trusted=config.SSL_CLIENT_CERT_FILE,
        )

    server = Server([NobetService(), Health()])

    with graceful_exit([server]):
        await server.start(config.SERVICE_ADDRESS, config.SERVICE_PORT, ssl=ssl_context)
        print("gRPC server running on "+str(config.SERVICE_ADDRESS)+':'+str(config.SERVICE_PORT)+"...")
        logger.info(
            "Node service running on %s:%i", config.SERVICE_ADDRESS, int(config.SERVICE_PORT)
        )
        await server.wait_closed()
