import os
from typing import Optional, List

from pkg_resources import DistributionNotFound, get_distribution
from tornado.routing import _RuleList
from tornado import ioloop

from mind.logging import get_logger
from mind.messaging import registry
from mind.models import AudioFrame, Text, VideoFrame
from mind.ai.chatbot import ChatBotListenerTask
from mind.ai.object_detection import ObjectDetectionListenerTask
from mind.ai.speech_to_text import SpeechToTextListenerTask
from mind.ai.text_to_speech import TextToSpeechListenerTask
from mind.devices.microphone import MicrophoneStreamTask
from mind.server.BoardWebSocketHandler import BoardWebSocketHandler, BoardWebSocketHandlerListenerTask
from mind.server.CameraWebHandler import CameraWebHandler
from mind.server.MqttWebHandler import MqttWebHandler


def setup_registry():
    registry.register_tasks(
        [
            ChatBotListenerTask,
            (ObjectDetectionListenerTask, (True, True)),
            SpeechToTextListenerTask,
            TextToSpeechListenerTask,
            BoardWebSocketHandlerListenerTask,
            MicrophoneStreamTask,
        ]
    )

    registry.register_listeners(
        [
            (ChatBotListenerTask, Text),
            (ObjectDetectionListenerTask, VideoFrame),
            (SpeechToTextListenerTask, AudioFrame),
            (TextToSpeechListenerTask, Text),
            (BoardWebSocketHandlerListenerTask, Text),
        ]
    )


routes: Optional[_RuleList] = [
    (r"/ws/(?P<board>[A-Za-z]+)", BoardWebSocketHandler),
    (r"/camera", CameraWebHandler),
    (r"/command", MqttWebHandler),
]

__author__ = "Jonas Lima"
__copyright__ = "Jonas Lima"
__license__ = "gpl"

try:
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
