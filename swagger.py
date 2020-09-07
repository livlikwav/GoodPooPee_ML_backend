swagger_config = {
    'openapi': '3.0.0',
    'doc_dir': './app/docs/'
}

swagger_template = {
    "info": {
        "description": "SWMaestro 11th, Team urillbwa, Goodpoopee. \
        \n Maintainer: Gyeongmin Ha.",
        "version": "2.0.0",
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
    }, "components": {
        "schemas": {
            "user_auth_token": {
                "type": "object",
                "properties": {
                    "access_token": {
                        "type": "string",
                        "example": "eyJ0dasd1g3V1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTk1Njc0MTMsImlhdCI6MTU5OTQ4MTAxMywic3ViIjoxfQ.ZSkYoZituRfGkoO44xNF7zDS01Dnk6IaTHVQOKNvzOg"
                    }
                }
            },
            "device_auth_token": {
                "type": "object",
                "properties": {
                    "device_access_token": {
                        "type": "string",
                        "example": "eyJ0dasd1g3V1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTk1Njc0MTMsImlhdCI6MTU5OTQ4MTAxMywic3ViIjoxfQ.ZSkYoZituRfGkoO44xNF7zDS01Dnk6IaTHVQOKNvzOg"
                    }
                }
            },
            "api_response": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "integer",
                        "format": "int32",
                        "example": "Success"
                    },
                    "message": {
                        "type": "string",
                        "example": "Success to ~~~"
                    }
                }
            },
            "api_fail_response": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "integer",
                        "format": "int32",
                        "example": "Fail"
                    },
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
                    },
                    "hashed_password": {
                        "type": "string",
                        "example": "qef211rgr2365h123sdfwert123123"
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
            "pet": {
                "type": "object",
                "required": ["petid"],
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64",
                        "example": "1"
                    },
                    "userId": {
                        "type": "string"
                    },
                    "petname": {
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
                    "adopt": {
                        "type": "string",
                        "example": "20001011"
                    }
                }
            },
            "pet_record": {
                "type": "object",
                "required": ["petId", "timestamp"],
                "properties": {
                    "petId": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "timestamp": {
                        "type": "string",
                        "example": "1970-01-01 00:00:01"
                    },
                    "result": {
                        "type": "string",
                        "example": "SUCCESS"
                    },
                    "photoUrl": {
                        "type": "string"
                    }
                }
            },
            "pet_daily_report": {
                "type": "object",
                "required": ["pet_id", "date"],
                "properties": {
                    "pet_id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "date": {
                        "type": "string",
                        "example": "DATE like YYYYMMDD"
                    },
                    "count": {
                        "type": "integer",
                        "example": "total pooing count like 10"
                    },
                    "success": {
                        "type": "integer",
                        "example": "success count like 5"
                    },
                    "progress": {
                        "type": "number",
                        "example": "progress ratio like 0~1%"
                    }
                }
            },
            "pet_weekly_report": {
                "type": "object",
                "required": ["pet_id", "lastdate"],
                "properties": {
                    "pet_id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "lastdate": {
                        "type": "string",
                        "example": "DATE like YYYYMMDD"
                    },
                    "count": {
                        "type": "integer",
                        "example": "total pooing count like 10"
                    },
                    "success": {
                        "type": "integer",
                        "example": "success count like 5"
                    },
                    "progress": {
                        "type": "number",
                        "example": "progress ratio like 0~1%"
                    }
                }
            },
            "pet_total_report": {
                "type": "object",
                "required": ["pet_id"],
                "properties": {
                    "pet_id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "count": {
                        "type": "integer",
                        "example": "total pooing count like 10"
                    },
                    "success": {
                        "type": "integer",
                        "example": "success count like 5"
                    },
                    "progress": {
                        "type": "number",
                        "example": "progress ratio like 0~1%"
                    },
                    "start_date": {
                        "type": "string",
                        "example": "20200501"
                    },
                    "last_date": {
                        "type": "string",
                        "example": "20200702"
                    }
                }
            },
            "ppcam": {
                "type": "object",
                "required": ["ppcamId", "userId", "serialNum"],
                "properties": {
                    "ppcamId": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "userId": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "serialNum": {
                        "type": "integer",
                        "format": "int64"
                    }
                }
            },
            "pad": {
                "type": "object",
                "required": ["padId", "ppcamId", "lu", "ld", "ru", "rd"],
                "properties": {
                    "padId": {
                        "type": "integer"
                    },
                    "ppcamId": {
                        "type": "integer"
                    },
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
                    }
                }
            },
            "ppsnack": {
                "type": "object",
                "required": ["ppcamId", "serialNum"],
                "properties": {
                    "ppcamId": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "serialNum": {
                        "type": "integer",
                        "format": "int64"
                    }
                }
            },
            "ppsnack_config": {
                "type": "object",
                "required": ["ppcamId", "onoff", "ratio"],
                "properties": {
                    "ppcamId": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "onoff": {
                        "type": "boolean",
                        "example": "True of False"
                    },
                    "ratio": {
                        "type": "number",
                        "example": "0~1 %"
                    }
                }
            }
        }
    }
}
