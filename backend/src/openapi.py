"""
OpenAPI specification and documentation configuration.
"""
from typing import Dict, Any
from quart import Quart
from src.config import settings


def get_openapi_spec() -> Dict[str, Any]:
    """
    Generate OpenAPI 3.0 specification for the API.

    Returns:
        OpenAPI specification dictionary
    """
    return {
        "openapi": "3.0.3",
        "info": {
            "title": settings.app_name,
            "description": (
                "API for the CodeMentor LLM Coding Tutor Platform. "
                "Provides endpoints for user authentication, daily coding exercises, "
                "chat-based tutoring, GitHub code reviews, and progress tracking."
            ),
            "version": "0.1.0",
            "contact": {
                "name": "CodeMentor API Support",
                "email": "api@codementor.io"
            },
            "license": {
                "name": "Internal - All Rights Reserved"
            }
        },
        "servers": [
            {
                "url": f"http://{settings.host}:{settings.port}/api/v1",
                "description": "Development server"
            },
            {
                "url": "/api/v1",
                "description": "Current server"
            }
        ],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "JWT access token obtained from /auth/login or /auth/register"
                }
            },
            "schemas": {
                "Error": {
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "string",
                                    "example": "VALIDATION_ERROR"
                                },
                                "message": {
                                    "type": "string",
                                    "example": "Request validation failed"
                                },
                                "details": {
                                    "type": "object"
                                }
                            }
                        }
                    }
                },
                "User": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "example": 1
                        },
                        "email": {
                            "type": "string",
                            "format": "email",
                            "example": "user@example.com"
                        },
                        "name": {
                            "type": "string",
                            "example": "John Doe"
                        },
                        "role": {
                            "type": "string",
                            "enum": ["student", "mentor", "moderator", "admin"],
                            "example": "student"
                        },
                        "programming_language": {
                            "type": "string",
                            "example": "python"
                        },
                        "skill_level": {
                            "type": "string",
                            "enum": ["beginner", "intermediate", "advanced", "expert"],
                            "example": "intermediate"
                        },
                        "created_at": {
                            "type": "string",
                            "format": "date-time"
                        }
                    }
                },
                "Exercise": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "example": 1
                        },
                        "title": {
                            "type": "string",
                            "example": "Binary Search Implementation"
                        },
                        "description": {
                            "type": "string",
                            "example": "Implement binary search algorithm"
                        },
                        "difficulty": {
                            "type": "string",
                            "enum": ["easy", "medium", "hard", "expert"],
                            "example": "medium"
                        },
                        "language": {
                            "type": "string",
                            "example": "python"
                        },
                        "topic": {
                            "type": "string",
                            "example": "algorithms"
                        }
                    }
                },
                "Message": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "example": 1
                        },
                        "role": {
                            "type": "string",
                            "enum": ["user", "assistant", "system"],
                            "example": "user"
                        },
                        "content": {
                            "type": "string",
                            "example": "How do I implement a binary search?"
                        },
                        "created_at": {
                            "type": "string",
                            "format": "date-time"
                        }
                    }
                }
            }
        },
        "security": [
            {
                "bearerAuth": []
            }
        ],
        "paths": {
            "/health/": {
                "get": {
                    "summary": "Health check",
                    "tags": ["Health"],
                    "security": [],
                    "responses": {
                        "200": {
                            "description": "Service is healthy"
                        }
                    }
                }
            },
            "/auth/register": {
                "post": {
                    "summary": "Register new user",
                    "tags": ["Authentication"],
                    "security": [],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["email", "password", "name"],
                                    "properties": {
                                        "email": {
                                            "type": "string",
                                            "format": "email"
                                        },
                                        "password": {
                                            "type": "string",
                                            "minLength": 12
                                        },
                                        "name": {
                                            "type": "string"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "User registered successfully"
                        },
                        "400": {
                            "description": "Invalid request"
                        }
                    }
                }
            },
            "/auth/login": {
                "post": {
                    "summary": "Login user",
                    "tags": ["Authentication"],
                    "security": [],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["email", "password"],
                                    "properties": {
                                        "email": {
                                            "type": "string",
                                            "format": "email"
                                        },
                                        "password": {
                                            "type": "string"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Login successful"
                        },
                        "401": {
                            "description": "Invalid credentials"
                        }
                    }
                }
            }
        },
        "tags": [
            {
                "name": "Health",
                "description": "Health and readiness checks"
            },
            {
                "name": "Authentication",
                "description": "User authentication and session management"
            },
            {
                "name": "Users",
                "description": "User profile and preferences management"
            },
            {
                "name": "Exercises",
                "description": "Coding exercises and submissions"
            },
            {
                "name": "Chat",
                "description": "LLM tutor chat conversations"
            },
            {
                "name": "GitHub",
                "description": "GitHub repository integration and code reviews"
            }
        ]
    }


def setup_openapi_routes(app: Quart) -> None:
    """
    Set up OpenAPI documentation routes.

    Args:
        app: Quart application instance
    """

    @app.route("/openapi.json", methods=["GET"])
    async def openapi_spec():
        """Return OpenAPI specification as JSON."""
        return get_openapi_spec()

    @app.route("/docs", methods=["GET"])
    async def swagger_ui():
        """Serve Swagger UI for interactive API documentation."""
        # Simple HTML page with Swagger UI
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{settings.app_name} API Documentation</title>
            <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.10.0/swagger-ui.css" />
            <style>
                body {{ margin: 0; padding: 0; }}
            </style>
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist@5.10.0/swagger-ui-bundle.js"></script>
            <script src="https://unpkg.com/swagger-ui-dist@5.10.0/swagger-ui-standalone-preset.js"></script>
            <script>
                window.onload = function() {{
                    SwaggerUIBundle({{
                        url: "/openapi.json",
                        dom_id: '#swagger-ui',
                        deepLinking: true,
                        presets: [
                            SwaggerUIBundle.presets.apis,
                            SwaggerUIStandalonePreset
                        ],
                        plugins: [
                            SwaggerUIBundle.plugins.DownloadUrl
                        ],
                        layout: "StandaloneLayout"
                    }});
                }};
            </script>
        </body>
        </html>
        """
        return html, 200, {"Content-Type": "text/html"}
