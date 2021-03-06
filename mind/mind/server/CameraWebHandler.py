# import threading, queue

from tornado.queues import Queue, QueueFull
from tornado.web import RequestHandler

from mind.logging import get_logger
from mind.server.WebSocketHandler import WebSocketHandler

# from mind.ai.object_detection import ObjectDetection
from mind.models import VideoFrame

logger = get_logger(__name__)


class CameraWebHandler(RequestHandler):

    # object_detection = ObjectDetection()

    async def get(self):
        logger.info("Started stream")

        # async for packet in camera_queue:
        #     try:
        #         encoded_frame = self.object_detection.process_frames_from_bytes(packet.data)
        #         await self.stream_encoded_frame(encoded_frame)
        #     finally:
        #         camera_queue.task_done()

    async def stream_encoded_frame(self, encoded_frame) -> None:
        self.set_header("Cache-Control", "no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0")
        self.set_header("Connection", "close")
        self.set_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")

        self.write(b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + encoded_frame + b"\r\n")

        await self.flush()

    # def store_jpg(self, frame_in_bytes):
    #     import time
    #     import os
    #     now = int(time.time())
    #     file_name = os.path.join(os.path.dirname(__file__), "../../assets", f"{now}.jpg")

    #     logger.debug(f"Writing {len(frame_in_bytes)} bytes, {now}.jpg unix")
    #     print(file_name)

    #     f = open(file_name, 'wb')
    #     f.write(frame_in_bytes)
    #     f.close()
