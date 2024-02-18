package model.discord.gateway

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonElement

@Serializable
data class Event(
    @SerialName("op")
    val operation: Operation,

    @SerialName("t")
    val eventName: String?,

    @SerialName("s")
    val sequenceNumber: Int?,

    @SerialName("d")
    val payload: JsonElement?
)
