from interactions import Embed


class Failure(RuntimeError):
    def embed(self) -> Embed:
        raise NotImplementedError

