package util

import io.github.oshai.kotlinlogging.KLogger
import io.github.oshai.kotlinlogging.KotlinLogging
import kotlin.reflect.KClass

fun <T : Any> lazyLogger(kClass: KClass<T>): Lazy<KLogger> {
    val loggerName = kClass.qualifiedName!!
    return lazy { KotlinLogging.logger(loggerName) }
}
