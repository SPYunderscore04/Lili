import io.github.oshai.kotlinlogging.KotlinLogging
import kotlinx.coroutines.delay
import kotlinx.coroutines.runBlocking
import service.DiscordApi
import service.DiscordGateway
import kotlin.time.Duration.Companion.seconds

expect fun configurePlatform()

private val log by lazy { KotlinLogging.logger { } }

fun main() {
    configurePlatform()

    val result = runBlocking { DiscordApi.getBotGatewayInfo() }
    require(result.shards == 1) { "Bot became too popular too soon, sharding must now be implemented!" }

    log.info { "Result URL: ${result.url}" }

    // ---

    val gateway = DiscordGateway(result.url)
    log.info { "Gateway created: $gateway" }
    runBlocking { delay(10.seconds) }
}
