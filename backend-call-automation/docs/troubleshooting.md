# ElevenLabs Integration Troubleshooting Guide

This guide provides steps to diagnose and resolve common issues related to the ElevenLabs text-to-speech integration.

## Common Issues and Solutions

### 1. Connection Pool Exhaustion / High Latency

**Symptoms:**
*   Errors like "Timeout acquiring connection" or similar from the connection pool.
*   Increased `elevenlabs_request_duration_seconds` metric values.
*   Alert `ElevenLabsPoolNearExhaustion` or `ElevenLabsHighLatency` firing.

**Potential Causes:**
*   Insufficient pool size (`ELEVENLABS_MAX_CONNECTIONS`) for the current load.
*   Long-running requests holding connections.
*   Network issues between the application and ElevenLabs API.
*   ElevenLabs API experiencing performance degradation.

**Troubleshooting Steps:**
1.  **Monitor Metrics:** Check `elevenlabs_pool_connections_active` vs `elevenlabs_pool_size`. Is the pool consistently near or at capacity? Check `elevenlabs_request_duration_seconds` for high latency trends.
2.  **Check ElevenLabs Status:** Visit the [ElevenLabs Status Page](https://status.elevenlabs.io/) (or their official status source) for any ongoing incidents.
3.  **Review Logs:** Look for specific error messages in the `elevenlabs_service` logs (enabled by `ElevenLabsLogger`) around the time of the issue. Check for connection timeouts or API errors.
4.  **Analyze Load:** Is there an unusual spike in requests (`elevenlabs_requests_total`)?
5.  **Increase Pool Size:** If the load is consistently high and the API is stable, consider gradually increasing `ELEVENLABS_MAX_CONNECTIONS` in your environment settings. Monitor the impact.
6.  **Adjust Timeouts:** Review `ELEVENLABS_POOL_TIMEOUT` and `ELEVENLABS_CONNECTION_TIMEOUT`. Are they appropriate? Very short timeouts might cause issues under load, while very long ones might hold resources unnecessarily.

### 2. API Rate Limiting (429 Errors)

**Symptoms:**
*   `429 Too Many Requests` errors logged by `ElevenLabsLogger` or visible in metrics (`elevenlabs_errors_total{error_type="APIError"}` or similar, depending on how the library surfaces the error).
*   Alert `ElevenLabsHighErrorRate` might fire if 429s become frequent.

**Potential Causes:**
*   Exceeding the request limits defined by your ElevenLabs API plan tier.
*   Bursts of requests overwhelming the limit.

**Troubleshooting Steps:**
1.  **Check ElevenLabs Dashboard:** Log in to your ElevenLabs account and check your API usage statistics and limits.
2.  **Review Logs & Metrics:** Identify which methods (`generate_audio`, `generate_response`) are causing the rate limits. Check the frequency (`elevenlabs_requests_total`).
3.  **Implement Client-Side Rate Limiting/Throttling:** If possible, add delays or limits within the application before calling the API, especially for batch operations. The `with_retry` decorator already provides backoff, but might not be enough for hard rate limits.
4.  **Optimize API Calls:** Can requests be batched or made less frequently?
5.  **Upgrade API Tier:** If usage legitimately exceeds the current plan limits, consider upgrading your ElevenLabs subscription.

### 3. Audio Generation Failures (Non-429 Errors)

**Symptoms:**
*   Errors logged by `ElevenLabsLogger` (e.g., `APIError`, `ValueError`, `AuthenticationError`).
*   Alert `ElevenLabsHighErrorRate` or `ElevenLabsCriticalErrorRate` firing.
*   Empty (`b""`) or seemingly corrupted audio data returned.

**Potential Causes:**
*   Invalid API Key (`AuthenticationError`).
*   Invalid input parameters (e.g., unsupported voice ID, text too long, invalid characters).
*   Temporary issues with the ElevenLabs API.
*   Bugs in the service code interacting with the API.

**Troubleshooting Steps:**
1.  **Check Logs:** Examine the detailed error message and context logged by `ElevenLabsLogger` (`log_error`). This is the most crucial step.
2.  **Verify API Key:** Ensure `ELEVENLABS_API_KEY` (or the key fetched from Vault) is correct and has the necessary permissions in your ElevenLabs account. Check for expiration if applicable.
3.  **Validate Input:** Review the `params` logged for the failing request. Is the text valid? Is the voice ID correct? Are there any unusual characters?
4.  **Check ElevenLabs Status:** Verify if there are known issues with the API.
5.  **Test Directly:** Try making a similar request directly to the ElevenLabs API (e.g., using `curl` or Postman) with the same parameters to isolate the issue.
6.  **Review Code:** Double-check the code in `ElevenLabsService` around the failing method (`generate_audio`, `generate_response`, `start_conversation`) for any logic errors.
7.  **Check Dependencies:** Ensure the `elevenlabs` library is up-to-date (`pip show elevenlabs`).

## Monitoring and Debugging Tools

### Key Metrics (Prometheus)
*   `elevenlabs_requests_total`: Overall request volume and success/error status per method.
*   `elevenlabs_errors_total`: Frequency of specific error types.
*   `elevenlabs_request_duration_seconds`: Latency distribution for API calls.
*   `elevenlabs_pool_connections_active`: Current usage of the connection pool.
*   `elevenlabs_pool_size`: Configured maximum size of the pool.
*   `circuit_breaker_state` (from `FallbackService`): Indicates if the circuit breaker is open due to repeated failures.

### Log Analysis
*   **Structured Logs:** Check the output configured for the `elevenlabs_service` logger (created by `ElevenLabsLogger`). These logs are in JSON format and contain detailed context for API calls and errors. Search for `"service": "ElevenLabsService"` and filter by level (`ERROR`, `WARNING`, `INFO`).
*   **Application Logs:** Check the main application logs for related errors that might occur before or after calls to `ElevenLabsService`.
*   **Infrastructure Logs:** If running in containers or cloud environments, check logs from load balancers, gateways, or container orchestrators for network-related issues.

### Debugging
*   **Local Testing:** Reproduce the issue locally with debugging enabled.
*   **Mocks:** Use the mock classes (`MockConversation`, `MockVoiceSettings`) or `unittest.mock.patch` to isolate specific parts of the service during testing.
