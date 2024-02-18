package service

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.websocket.*
import io.ktor.websocket.*
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.Json
import model.discord.gateway.Event
import util.lazyLogger

private val log by lazyLogger(DiscordGateway::class)

class DiscordGateway(url: String) {

    private val client = HttpClient(CIO) {
        install(WebSockets)
    }

    init {
        runBlocking {
            client.webSocket(url) {
                val userInputRoutine = launch { __write(this@webSocket) }
                val messageOutputRoutine = launch { __read(this@webSocket) }

                userInputRoutine.join() // Wait for completion; either "exit" or error
                messageOutputRoutine.cancelAndJoin()
                // ^ TODO
            }

            client.close()
            log.info { "Client closed" }
        }
    }

    private suspend fun __write(session: DefaultClientWebSocketSession) {
        while (true) {
            // TODO
        }
    }

    private suspend fun __read(session: DefaultClientWebSocketSession) {
        try {
            for (message in session.incoming) {
                if (message is Frame.Text) {
                    val text = message.readText()
                    log.debug { "Received: $text" }

                    val event = Json.decodeFromString<Event>(text)
                    log.info { "Event: $event" }
                }
            }
        } catch (e: Exception) {
            log.error(e) { "Error receiving" }
        }
    }
}
