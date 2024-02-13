package util

import kotlinx.cinterop.ExperimentalForeignApi
import kotlinx.cinterop.toKString
import platform.posix.getenv

@OptIn(ExperimentalForeignApi::class)
actual fun getEnvVariable(name: String) =
    getenv(name)?.toKString() ?: throw EnvVariableMissing(name)
