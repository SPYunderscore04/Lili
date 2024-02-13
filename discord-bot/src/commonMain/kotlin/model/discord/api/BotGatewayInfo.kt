package model.discord.api

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class BotGatewayInfo(
    @SerialName("url")
    val url: String,

    @SerialName("session_start_limit")
    val sessionStartLimit: SessionStartLimit,

    @SerialName("shards")
    val shards: Int
)

@Serializable
data class SessionStartLimit(
    @SerialName("max_concurrency")
    val maxConcurrency: Int,

    @SerialName("remaining")
    val remaining: Int,

    @SerialName("reset_after")
    val resetAfter: Int,

    @SerialName("total")
    val total: Int
)
