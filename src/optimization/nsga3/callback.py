from pymoo.core.callback import Callback


class ContainerCallback(Callback):
    def notify(self, algorithm):
        print(f"Generation: {algorithm.n_gen}")
