import zmq
from imagezmq import imagezmq


class ImageSenderSmallQueue(imagezmq.ImageSender):
    def init_pubsub(self, address):
        socket_type = zmq.PUB
        self.zmq_context = imagezmq.SerializingContext()
        self.zmq_socket = self.zmq_context.socket(socket_type)
        self.zmq_socket.setsockopt(zmq.SNDHWM, 2)

        self.zmq_socket.bind(address)

        self.send_image = self.send_image_pubsub
        self.send_jpg   = self.send_jpg_pubsub