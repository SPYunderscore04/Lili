package model.discord.gateway

import kotlinx.serialization.KSerializer
import kotlinx.serialization.Serializable
import kotlinx.serialization.descriptors.PrimitiveKind
import kotlinx.serialization.descriptors.PrimitiveSerialDescriptor
import kotlinx.serialization.encoding.Decoder
import kotlinx.serialization.encoding.Encoder

/** See [https://discord.com/developers/docs/topics/opcodes-and-status-codes](https://discord.com/developers/docs/topics/opcodes-and-status-codes) */
@Serializable(with = OperationSerializer::class)
enum class Operation(val op: Int) {
    DISPATCH(0),
    HEARTBEAT(1),
    IDENTIFY(2),
    PRESENCE_UPDATE(3),
    VOICE_STATE_UPDATE(4),
    RESUME(6),
    RECONNECT(7),
    REQUEST_GUILD_MEMBERS(8),
    INVALID_SESSION(9),
    HELLO(10),
    HEARTBEAT_ACK(11)
}

private class OperationSerializer : KSerializer<Operation> {
    override val descriptor = PrimitiveSerialDescriptor(this::class.qualifiedName!!, PrimitiveKind.INT)

    override fun serialize(encoder: Encoder, value: Operation) =
        encoder.encodeInt(value.op)

    override fun deserialize(decoder: Decoder): Operation {
        val op = decoder.decodeInt()
        return Operation.entries.first { it.op == op }
    }
}
