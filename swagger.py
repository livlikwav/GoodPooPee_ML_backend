swagger_config = {
    'title': 'Goodpoopee server',
    'description': 'For poopeecam, poopeesnackbar and goodpoopee app.',
    'uiversion': 3,
    'openapi': '3.0.2',
    # 'doc_dir': './app/docs',
    'components': {
        'schemas': {
            "ApiResponse": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "integer",
                        "format": "int32"
                    },
                    "message": {
                        "type": "string",
                        "example": "Success to ~~~"
                    }
                }
            },
            "ApiFailResponse": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "integer",
                        "format": "int32"
                    },
                    "message": {
                        "type": "string",
                        "example": "Fail to ~~~"
                    }
                }
            },
            "ppcam": {
                "required": ["mac_address", "serial_num", "user_id"],
                "type": "object",
                "properties": {
                    "serial_num": {
                        "type": "string",
                        "example": "asd1234567893333"
                    },
                    "mac_address": {
                        "type": "string",
                        "example": "98e08f333823"
                    },
                    "user_id": {
                        "type": "integer",
                        "format": "int64"
                    }
                }
            },
            "device_auth_token": {
                "required": ["token"],
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "example": "asd1234asd5678933qgs33"
                    }
                }
            },
            "pad": {
                "required": ["ld", "lu", "ppcam_id", "rd", "ru", "user_id"],
                "type": "object",
                "properties": {
                    "lu": {
                        "type": "integer"
                    },
                    "ld": {
                        "type": "integer"
                    },
                    "ru": {
                        "type": "integer"
                    },
                    "rd": {
                        "type": "integer"
                    },
                    "user_id": {
                        "type": "integer"
                    },
                    "ppcam_id": {
                        "type": "integer"
                    }
                }
            },
            "ppsnack_config": {
                "required": ["feedback_ratio", "ppcam_id", "serial_num"],
                "type": "object",
                "properties": {
                    "serial_num": {
                        "type": "string",
                        "example": "ADW23123124124"
                    },
                    "feedback_ratio": {
                        "type": "number"
                    },
                    "ppcam_id": {
                        "type": "integer",
                        "format": "int64"
                    }
                }
            },
            "pet_record": {
                "required": ["image_uuid", "pet_id", "result", "user_id"],
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "pet_id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "result": {
                        "type": "string",
                        "example": "Success"
                    },
                    "image_uuid": {
                        "type": "string",
                        "example": "3edfba2f-e180-45ed-b60d-58ef7fb35c96"
                    }
                }
            },
        }
    }
}
