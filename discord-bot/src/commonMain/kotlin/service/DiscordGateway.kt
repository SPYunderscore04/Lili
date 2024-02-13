package service

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.websocket.*
import io.ktor.websocket.*
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

class DiscordGateway(
    url: String
) {

    private val client = HttpClient(CIO) {
        install(WebSockets)
    }

    init {
        runBlocking {
            client.webSocket(url) {
                val userInputRoutine = launch { inputMessages() }
                val messageOutputRoutine = launch { outputMessages() }

                userInputRoutine.join() // Wait for completion; either "exit" or error
                messageOutputRoutine.cancelAndJoin()
            }
        }
        client.close()
        println("Connection closed. Goodbye!")
    }

    private suspend fun DefaultClientWebSocketSession.inputMessages() {
        while (true) {
            val message = readlnOrNull() ?: ""
            if (message.equals("exit", true)) return
            try {
                send(message)
            } catch (e: Exception) {
                println("Error while sending: $e")
            }
        }
    }

    private suspend fun DefaultClientWebSocketSession.outputMessages() {
        try {
            for (message in incoming) {
                message as? Frame.Text
                    ?: continue
                println(message.readText())
            }
        } catch (e: Exception) {
            println("Error while receiving: $e")
        }
    }
}
