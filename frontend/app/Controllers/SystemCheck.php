<?php

namespace App\Controllers;

use App\Libraries\ApiClient;
use CodeIgniter\HTTP\ResponseInterface;

class SystemCheck extends BaseController
{
    public function backend(): ResponseInterface
    {
        $apiClient = new ApiClient();

        $result = $apiClient->get('/health');

        return $this->response
            ->setStatusCode(
                $result['success'] ? 200 : 503
            )
            ->setJSON([
                'frontend' => 'connected',
                'backend'  => $result,
            ]);
    }
}