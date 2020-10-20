swagger_config = {
    'openapi': '3.0.2',
    'doc_dir': './app/docs/'
}

swagger_template = {
    "info": {
        "description": "SWMaestro 11th, Team urillbwa, Goodpoopee. \
        \n Maintainer: Gyeongmin Ha.\
        \n API versioning V[major].[minor]",
        "version": "2.0", # API version
        "termsOfService": "",
        "contact": {
            "email": "gaonrudal@gmail.com"
        },
        # "license": {
        #     "name": "Apache 2.0",
        #     "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        # },
        "title": "Good-poopee Server"
    },
    "servers": [{
        "description": "SwaggerHub API Auto Mocking",
        "url": "https://virtserver.swaggerhub.com/livlikwav.github.io/goodpoopee/1.0.0"
    }],
    "tags": [{
        "name": "user",
        "description": "Operations about user"
    }, {
        "name": "pet",
        "description": "Operations about pets"
    }, {
        "name": "ppcam",
        "description": "Operations about poopee cam"
    }],

    "externalDocs": {
        "description": "Rest API design note",
        "url": "https://docs.google.com/document/d/1CHvAOqb5mZXAMF3kW0egfUHieE0xZS5YCmDZ-UT2INI/edit?usp=sharing"
    },
    
    "components": {
        "securitySchemes":{
            "user_auth": {
                "type" : "http",
                "scheme" : "bearer",
                "bearerFormat" : "JWT"
            },
            "device_auth":{
                "type" : "http",
                "scheme" : "bearer",
                "bearerFormat" : "JWT"
            }
        },
        "schemas": {
            # for user login api's response schema
            "user_log_in": {
                "type": "object",
                "properties": {
                    "access_token": {
                        "type": "string",
                        "example": "eyJ0dasd1g3V1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTk1Njc0MTMsImlhdCI6MTU5OTQ4MTAxMywic3ViIjoxfQ.ZSkYoZituRfGkoO44xNF7zDS01Dnk6IaTHVQOKNvzOg"
                    },
                    "user" : {
                        "type" : "object",
                        "$ref" : "#/components/schemas/user"
                    },
                    "pet" : {
                        "type" : "object",
                        "$ref" : "#/components/schemas/pet",
                    }
                }
            },
            "device_log_in": {
                "type": "object",
                "properties": {
                    "device_access_token": {
                        "type": "string",
                        "example": "eyJ0dasd1g3V1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTk1Njc0MTMsImlhdCI6MTU5OTQ4MTAxMywic3ViIjoxfQ.ZSkYoZituRfGkoO44xNF7zDS01Dnk6IaTHVQOKNvzOg"
                    },
                    "ppcam_id" : {
                        "type" : "integer",
                        "format" : "int32"
                    },
                    "user_id" : {
                        "type" : "integer",
                        "format" : "int32"
                    },
                    "pet_id" : {
                        "type" : "integer",
                        "format" : "int32"
                    }
                }
            },
            "feeding": {
                "type": "object",
                "properties": {
                    "feeding": {
                        "type": "integer",
                        "format" : "int32",
                        "example" : 3
                    }
                }
            },
            "api_response": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Success to ~~~"
                    }
                }
            },
            "api_fail_response": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Fail to ~~~"
                    }
                }
            },
            "register_user": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "example": "gaonrudal@gmail.com"
                    },
                    "first_name": {
                        "type": "string",
                        "example": "Gyeongmin"
                    },
                    "last_name": {
                        "type": "string",
                        "example": "Ha"
                    },
                    "password": {
                        "type": "string",
                        "example": "123"
                    }
                }
            },
            "login_user": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "example": "gaonrudal@gmail.com"
                    },
                    "password": {
                        "type": "string",
                        "example": "123"
                    }
                }
            },
            "login_device": {
                "type": "object",
                "properties": {
                    "serial_num": {
                        "type": "string",
                        "example": "PC1K1P210101N001"
                    }
                }
            },
            "user": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64",
                        "example": "1"
                    },
                    "email": {
                        "type": "string",
                        "example": "gaonrudal@gmail.com"
                    },
                    "first_name": {
                        "type": "string",
                        "example": "Gyeongmin"
                    },
                    "last_name": {
                        "type": "string",
                        "example": "Ha"
                    }
                }
            },
            "register_pet": {
                "type": "object",
                "required": ["petid"],
                "properties": {
                    "user_id": {
                        "type": "string",
                        "example": "1"
                    },
                    "name": {
                        "type": "string",
                        "example": "mungchi"
                    },
                    "breed": {
                        "type": "string",
                        "example": "poodle"
                    },
                    "gender": {
                        "type": "string",
                        "example": "male"
                    },
                    "birth": {
                        "type": "string",
                        "example": "19981011"
                    },
                    "adoption": {
                        "type": "string",
                        "example": "20001011"
                    }
                }
            },
            "pet": {
                "type": "object",
                "required": ["petid"],
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64",
                        "example": "1"
                    },
                    "user_id": {
                        "type": "string",
                        "example": "1"
                    },
                    "name": {
                        "type": "string",
                        "example": "mungchi"
                    },
                    "breed": {
                        "type": "string",
                        "example": "poodle"
                    },
                    "gender": {
                        "type": "string",
                        "example": "male"
                    },
                    "birth": {
                        "type": "string",
                        "example": "2020-08-15T16:28:39"
                    },
                    "adoption": {
                        "type": "string",
                        "example": "2020-08-15T16:28:39"
                    }
                }
            },
            "pet_record": {
                "type": "object",
                "required": ["timestamp", "user_id", "pet_id", "result", "image_uuid", "created_date", "last_modified_date"],
                "properties": {
                    "timestamp": {
                        "type": "string",
                        "example": "2020-08-15T16:28:39"
                    },
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
                    },
                    "created_date": {
                        "type": "string",
                        "example": "2020-08-15T16:28:39"
                    },
                    "last_modified_date": {
                        "type": "string",
                        "example": "2020-08-15T16:28:39"
                    }
                }
            },
            "pet_daily_report": {
                "type": "object",
                "properties": {
                    "pet_id": {
                        "type": "integer",
                        "format": "int64",
                        "example": "1"
                    },
                    "user_id": {
                        "type": "integer",
                        "format": "int64",
                        "example": "1"
                    },
                    "date": {
                        "type": "string",
                        "example": "DATE like 2015-11-09"
                    },
                    "count": {
                        "type": "integer",
                        "example": "total pooing count like 10"
                    },
                    "success": {
                        "type": "integer",
                        "example": "success count like 5"
                    },
                    "ratio": {
                        "type": "number",
                        "example": "progress ratio like 0~1.0"
                    },
                    "created_date": {
                        "type": "string",
                        "example": "2020-08-15T16:28:39"
                    },
                    "last_modified_date": {
                        "type": "string",
                        "example": "2020-08-15T16:28:39"
                    }
                }
            },
            "pet_monthly_report": {
                "type": "object",
                "properties": {
                    "pet_id": {
                        "type": "integer",
                        "format": "int64",
                        "example": "1"
                    },
                    "user_id": {
                        "type": "integer",
                        "format": "int64",
                        "example": "1"
                    },
                    "date": {
                        "type": "string",
                        "example": "DATE like 2015-11-09"
                    },
                    "count": {
                        "type": "integer",
                        "example": "total pooing count like 10"
                    },
                    "success": {
                        "type": "integer",
                        "example": "success count like 5"
                    },
                    "ratio": {
                        "type": "number",
                        "example": "progress ratio like 0~1.0"
                    },
                    "created_date": {
                        "type": "string",
                        "example": "2020-08-15T16:28:39"
                    },
                    "last_modified_date": {
                        "type": "string",
                        "example": "2020-08-15T16:28:39"
                    }
                }
            },
            "total_month_report": {
                "type": "array",
                "items" : {
                    "$ref" : "#/components/schemas/pet_monthly_report"
                }
            },
            "ppcam": {
                "type": "object",
                "required": ["id", "user_id", "serial_num", "ip_address", "created_date", "last_modified_date"],
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "user_id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "serial_num": {
                        "type": "string",
                        "example": "PC1K1P210101N001"
                    },
                    "ip_address": {
                        "type": "string",
                        "example": "172.172.172.172",
                    },
                    "created_date": {
                        "type": "string",
                        "example": "2020-08-15T16:28:39"
                    },
                    "last_modified_date": {
                        "type": "string",
                        "example": "2020-08-15T16:28:39"
                    }
                }
            },
            "register_ppcam": {
                "type": "object",
                "required": ["ip_address", "user_id", "serial_num"],
                "properties": {
                    "ip_address": {
                        "type": "String",
                        "example" : "172.172.172.172"
                    },
                    "user_id": {
                        "type": "integer",
                        "format": "int32"
                    },
                    "serial_num": {
                        "type": "String",
                        "example": "PC1K1P210101N001",
                    }
                }
            },
            "pad": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "user_id": {
                        "type": "integer"
                    },
                    "ppcam_id": {
                        "type": "integer"
                    },
                    "lux": {
                        "type": "integer"
                    },
                    "luy": {
                        "type": "integer"
                    },
                    "ldx": {
                        "type": "integer"
                    },
                    "ldy": {
                        "type": "integer"
                    },
                    "rux": {
                        "type": "integer"
                    },
                    "ruy": {
                        "type": "integer"
                    },
                    "rdx": {
                        "type": "integer"
                    },
                    "rdy": {
                        "type": "integer"
                    }
                }
            },
            "register_pad": {
                "type": "object",
                "required": ["lux", "luy", "ldx", "ldy", "rux", "ruy", "rdx", "rdy"],
                "properties": {
                    "lux": {
                        "type": "integer"
                    },
                    "luy": {
                        "type": "integer"
                    },
                    "ldx": {
                        "type": "integer"
                    },
                    "ldy": {
                        "type": "integer"
                    },
                    "rux": {
                        "type": "integer"
                    },
                    "ruy": {
                        "type": "integer"
                    },
                    "rdx": {
                        "type": "integer"
                    },
                    "rdy": {
                        "type": "integer"
                    }
                }
            },
            "ppsnack": {
                "type": "object",
                "required": ["id", "ppcam_id", "user_id", "serial_num", "feedback"],
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "ppcam_id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "user_id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "serial_num": {
                        "type": "string",
                        "example": "PC1K1P210101N001"
                    },
                    "feedback": {
                        "type": "float",
                        "example": "0.0 ~ 1.0",
                    },
                    "created_date": {
                        "type": "string",
                        "example": "2020-08-15T16:28:39"
                    },
                    "last_modified_date": {
                        "type": "string",
                        "example": "2020-08-15T16:28:39"
                    }
                }
            },
            "put_ppsnack": {
                "type": "object",
                "required": ["feedback"],
                "properties": {
                    "feedback": {
                        "type": "float",
                        "example": "0.0 ~ 1.0",
                    }
                }
            },
            "polling": {
                "type": "object",
                "properties": {
                    "ppsnack" : {
                        "type" : "object",
                        "$ref" : "#/components/schemas/ppsnack"
                    },
                    "pad" : {
                        "type" : "object",
                        "$ref" : "#/components/schemas/pad"
                    },
                    "feeding" : {
                        "type" : "integer",
                        "example" : 3
                    },
                }
            },
            "stream_info": {
                "type": "object",
                "required": ["user_id", "ppcam_id", "user_ip"],
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "format": "int64",
                        "example": "1"
                    },
                    "ppcam_id": {
                        "type": "integer",
                        "format": "int64",
                        "example": "1"
                    },
                    "user_ip": {
                        "type": "string",
                        "example": "127.0.0.1"
                    }
                }
            }
        }
    }
}
