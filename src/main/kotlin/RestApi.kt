import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response

enum class RequestMethod { GET, POST, PUT, PATCH, DELETE }

open class RestApi(
    private val baseUrl: String,
    private val persistentHeaders: Map<String, String> = mapOf()
) {
    private val client = OkHttpClient()

    private fun requestOf(
        method: RequestMethod,
        path: String = "",
        body: String? = null,
        headers: Map<String, String> = mapOf(),
    ): Request {
        when (method) {
            RequestMethod.GET,
            RequestMethod.DELETE -> require(body == null)
            RequestMethod.POST,
            RequestMethod.PUT,
            RequestMethod.PATCH -> require(body != null)
        }

        val req = Request.Builder()

        // URL
        req.url(baseUrl + path)

        // Body
        when (method) {
            RequestMethod.GET -> req.get()
            RequestMethod.POST -> req.post(body!!.toRequestBody())
            RequestMethod.PUT -> req.put(body!!.toRequestBody())
            RequestMethod.PATCH -> req.patch(body!!.toRequestBody())
            RequestMethod.DELETE -> req.delete()
        }

        // Headers (user overrides persistent)
        for ((k, v) in persistentHeaders + headers) req.addHeader(k, v)

        return req.build()
    }

    fun get(
        path: String,
        headers: Map<String, String> = mapOf()
    ): Response = client
        .newCall(
            requestOf(
                method = RequestMethod.GET,
                path = path,
                headers = headers
            )
        ).execute()

    fun post(
        path: String,
        body: String,
        headers: Map<String, String> = mapOf()
    ): Response = client
        .newCall(
            requestOf(
                method = RequestMethod.POST,
                path = path,
                body = body,
                headers = headers
            )
        ).execute()

    fun put(
        path: String,
        body: String,
        headers: Map<String, String> = mapOf()
    ): Response = client
        .newCall(
            requestOf(
                method = RequestMethod.PUT,
                path = path,
                body = body,
                headers = headers
            )
        ).execute()

    fun patch(
        path: String,
        body: String,
        headers: Map<String, String> = mapOf()
    ): Response = client
        .newCall(
            requestOf(
                method = RequestMethod.PATCH,
                path = path,
                body = body,
                headers = headers
            )
        ).execute()

    fun delete(
        path: String,
        headers: Map<String, String> = mapOf()
    ): Response = client
        .newCall(
            requestOf(
                method = RequestMethod.DELETE,
                path = path,
                headers = headers
            )
        ).execute()
}
