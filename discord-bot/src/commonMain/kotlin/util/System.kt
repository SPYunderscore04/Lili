package util

expect fun getEnvVariable(name: String): String

fun envVariableMissing(name: String): Nothing = error("Environment $name is not set")
