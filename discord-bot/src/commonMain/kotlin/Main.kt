import kotlinx.coroutines.runBlocking
import service.DiscordApi
import service.DiscordGateway

expect fun configurePlatform()

fun main() {
    configurePlatform()

    val result = runBlocking { DiscordApi.getBotGatewayInfo() }
    require(result.shards == 1) { "Bot became too popular, sharding must now be implemented!" }

    println(result.url)

    // ---

    val gateway = DiscordGateway("wss://localhost:8080")
    println("Gateway created: $gateway")
}
