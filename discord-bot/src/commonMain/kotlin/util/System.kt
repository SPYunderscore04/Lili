package util

expect fun getEnvVariable(name: String): String

class EnvVariableMissing(name: String): IllegalStateException("Environment variable $name is not set")
