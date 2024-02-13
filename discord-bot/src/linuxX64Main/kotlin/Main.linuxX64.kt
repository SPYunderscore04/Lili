import io.github.oshai.kotlinlogging.KotlinLoggingConfiguration
import io.github.oshai.kotlinlogging.Level

actual fun configurePlatform() {
    KotlinLoggingConfiguration.logLevel = Level.DEBUG
}
