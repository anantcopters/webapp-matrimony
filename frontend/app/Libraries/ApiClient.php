<?php

namespace App\Libraries;

use CodeIgniter\HTTP\CURLRequest;
use Config\Services;
use RuntimeException;
use Throwable;

class ApiClient
{
    private CURLRequest $client;
    private string $baseUrl;

    public function __construct()
    {
        $baseUrl = env('API_BASE_URL');

        if (empty($baseUrl)) {
            throw new RuntimeException(
                'API_BASE_URL is not configured in the frontend .env file.'
            );
        }

        $this->baseUrl = rtrim($baseUrl, '/');

        $this->client = Services::curlrequest([
            'timeout'         => 10,
            'connect_timeout' => 3,
            'http_errors'     => false,
        ]);
    }

    public function get(string $endpoint): array
    {
        try {
            $response = $this->client->get(
                $this->baseUrl . '/' . ltrim($endpoint, '/'),
                [
                    'headers' => [
                        'Accept' => 'application/json',
                    ],
                ]
            );

            $body = json_decode(
                $response->getBody(),
                true,
                512,
                JSON_THROW_ON_ERROR
            );

            return [
                'success'     => $response->getStatusCode() >= 200
                    && $response->getStatusCode() < 300,
                'status_code' => $response->getStatusCode(),
                'data'        => $body,
            ];
        } catch (Throwable $exception) {
            log_message(
                'error',
                'FastAPI connection failed: {message}',
                ['message' => $exception->getMessage()]
            );

            return [
                'success'     => false,
                'status_code' => 0,
                'data'        => [
                    'status'  => 'error',
                    'message' => 'Unable to connect to the backend API.',
                ],
            ];
        }
    }
}