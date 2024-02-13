package util

actual fun getEnvVariable(name: String): String =
    System.getenv(name) ?: envVariableMissing(name)
