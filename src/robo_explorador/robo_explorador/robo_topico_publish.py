import random

import rclpy
from rclpy.node import Node
from robo_interfaces.msg import Monitoramento


class RoboTopicoPublish(Node):
    def __init__(self):
        super().__init__("robo_topico_publish")
        self.pub = self.create_publisher(Monitoramento, "monitoramento", 10)
        self.create_timer(1.0, self.publicar)
        self.get_logger().info("Robo publicando em /monitoramento")

    def publicar(self):
        msg = Monitoramento()
        msg.oxigenio = random.uniform(1, 100)
        msg.temperatura = random.uniform(1, 100)
        self.pub.publish(msg)
        self.get_logger().info(
            f"Publicado: oxigenio={msg.oxigenio:.1f} temperatura={msg.temperatura:.1f}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = RoboTopicoPublish()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == "__main__":
    main()