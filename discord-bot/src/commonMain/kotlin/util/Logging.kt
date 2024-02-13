package util

import io.github.oshai.kotlinlogging.KotlinLogging

fun <T : Any> getLogger(obj: T) = KotlinLogging.logger(obj::class.qualifiedName!!)
