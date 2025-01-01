from asyncio import Lock, sleep
from typing import TypeVar, Self

T = TypeVar("T")


class ValueLock[T]:
    def __init__(self):
        self._lock = Lock()

        self._values: list[T] = []
        self._full_lock = False

    def lock(self, value: T) -> "SingleLock[T]":
        return SingleLock(self, value)

    def lock_all(self) -> "FullLock[T]":
        return FullLock(self)

    async def acquire(self, value) -> None:
        while True:
            async with self._lock:
                if not self._full_lock and value not in self._values:
                    self._values.append(value)
                    return

            await sleep(0)

    async def acquire_all(self) -> None:
        while True:
            async with self._lock:
                if not self._full_lock and len(self._values) == 0:
                    self._full_lock = True
                    return

            await sleep(0)

    async def downgrade(self, value) -> None:
        async with self._lock:
            if not self._full_lock:
                raise RuntimeError("Must hold full lock to downgrade")

            self._full_lock = False
            self._values.append(value)

    async def release(self, value) -> None:
        async with self._lock:
            if value not in self._values:
                raise RuntimeError(f"Value {value} was not locked")

            self._values.remove(value)

    async def release_all(self) -> None:
        async with self._lock:
            if not self._full_lock:
                raise RuntimeError("Must hold full lock to release it")

            self._full_lock = False


class SingleLock[T]:
    def __init__(self, parent: ValueLock[T], value: T) -> None:
        self.parent = parent
        self.value = value

    async def __aenter__(self) -> None:
        await self.parent.acquire(self.value)

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.parent.release(self.value)


class FullLock[T]:
    def __init__(self, parent: ValueLock[T]):
        self.parent = parent
        self.value: T = None
        self.was_downgraded = False

    async def __aenter__(self) -> Self:
        await self.parent.acquire_all()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.was_downgraded:
            await self.parent.release(self.value)
        else:
            await self.parent.release_all()

    async def downgrade(self, value: T) -> None:
        if self.was_downgraded:
            raise RuntimeError("Already downgraded")

        self.value = value
        await self.parent.downgrade(value)
        self.was_downgraded = True
