swagger_config = {
    'openapi' : '3.0.0',
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
    },
    "components": {
        "schemas": {
            "user": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "email": {
                        "type": "string"
                    },
                    "first_name": {
                        "type": "string"
                    },
                    "last_name": {
                        "type": "string"
                    },
                    "password": {
                        "type": "string"
                    }
                }
            },
            "pet": {
                "type": "object",
                "required": ["petid"],
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64"
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
