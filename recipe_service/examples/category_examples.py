category_examples = {
    "create": {
        "requestBody": {
            "examples": {
                "fruits": {
                    "summary": "Create category 'Fruits'",
                    "description": "Category for fruits",
                    "value": {"name": "Fruits"},
                },
                "vegetables": {
                    "summary": "Create category 'Vegetables'",
                    "description": "Category for vegetables",
                    "value": {"name": "Vegetables"},
                },
            }
        },
        "responses": {
            200: {
                "description": "Category successfully created",
                "content": {
                    "application/json": {
                        "example": {"id": 1, "name": "Fruits"},
                    }
                },
            }
        },
    },

    "get_all": {
        "responses": {
            200: {
                "description": "Category list",
                "content": {
                    "application/json": {
                        "example": [
                            {"id": 1, "name": "Fruits"},
                            {"id": 2, "name": "Vegetables"},
                            {"id": 3, "name": "Dairy"},
                        ]
                    }
                },
            }
        },
    },

    "get_one": {
        "responses": {
            200: {
                "description": "Get category by ID",
                "content": {
                    "application/json": {
                        "example": [
                            {"id": 1, "name": "Fruits"},
                        ]
                    }
                },
            }
        },
    },

    "update": {
        "requestBody": {
            "examples": {
                "rename": {
                    "summary": "Rename category",
                    "value": {"name": "Exotic fruits"},
                }
            }
        },
        "responses": {
            200: {
                "description": "Category successfully updated",
                "content": {
                    "application/json": {
                        "example": {"id": 1, "name": "Exotic fruits"},
                    }
                },
            }
        },
    },

    "delete": {
        "responses": {
            200: {
                "description": "Category successfully deleted",
                "content": {
                    "application/json": {
                        "example": {"result": True, "message": "Category deleted"},
                    }
                },
            }
        },
    },
}