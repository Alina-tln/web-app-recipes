ingredient_examples = {
    "create": {
        "requestBody": {
            "examples": {
                "cheese": {
                    "summary": "Create ingredient 'Cheese'",
                    "description": "Create ingredient with a category",
                    "value": {
                        "name": "Cheese",
                        "category_ids": [1,2]
                    },
                }
            }
        },
        "responses": {
            200: {
                "description": "Ingredient successfully created",
                "content": {
                    "application/json": {
                        "example": {"id": 1, "name": "Cheese"},
                    }
                },
            }
        },
    },

    "get_all": {
        "responses": {
            200: {
                "description": "Ingredient list",
                "content": {
                    "application/json": {
                        "example": [
                            {"id": 1, "name": "Cheese", "category_ids": [1,2]},
                            {"id": 2, "name": "Milk", "category_ids": [1]},
                            {"id": 3, "name": "Prosciutto", "category_ids": [2]},
                        ]
                    }
                },
            }
        },
    },

    "get_one": {
        "responses": {
            200: {
                "description": "Get ingredient by ID",
                "content": {
                    "application/json": {
                        "example": [
                            {"id": 1, "name": "Cheese", "category_ids": [1,2]}
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
                    "summary": "Change ingredient",
                    "value": {"name": "Mozzarella", "category_ids": [3]}
                }
            }
        },
        "responses": {
            200: {
                "description": "Ingredient successfully updated",
                "content": {
                    "application/json": {
                        "example": {"id": 1, "name": "Mozzarella", "category_ids": [3]},
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
                        "example": {"result": True, "message": "Ingredient deleted"},
                    }
                },
            }
        },
    },
}