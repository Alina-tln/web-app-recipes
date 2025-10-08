ingredient_examples = {
    "create": {
        "requestBody": {
            "examples": {
                "cheese": {
                    "summary": "Create ingredient 'Cheese'",
                    "description": "Create ingredient with a category",
                    "value": {
                        "name": "Cheese",
                        "categories": [{"id": 1,
                                        "name": "Dairy"}]
                    },
                }
            }
        },
        "responses": {
            200: {
                "description": "Ingredient successfully created",
                "content": {
                    "application/json": {
                        "example": {"id": 1, "name": "Cheese", "categories": [{"id": 1, "name": "Dairy"}]},
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
                            {"id": 1,
                             "name": "Cheese",
                             "categories": [{"id": 1,
                                            "name": "Dairy"},
                                            {"id": 2,
                                             "name": "Snacks"}]
                             },
                            {"id": 2,
                             "name": "Milk",
                             "categories": [{"id": 1,
                                             "name": "Dairy"}]
                             },
                            {"id": 3,
                             "name": "Prosciutto",
                             "categories": [{"id": 2,
                                             "name": "Snacks"}]
                             },
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
                            {"id": 1,
                             "name": "Cheese",
                             "categories": [{"id": 1,
                                             "name": "Dairy"},
                                            {"id": 2,
                                             "name": "Snacks"}]
                             }
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
                    "value": {"name": "Mozzarella",
                              "categories": [{"id": 1,
                                             "name": "Dairy"}]
                              }
                }
            }
        },
        "responses": {
            200: {
                "description": "Ingredient successfully updated",
                "content": {
                    "application/json": {
                        "example": {"id": 1, "name": "Mozzarella",
                                    "categories": [{"id": 1,
                                                    "name": "Dairy"}]
                                    },
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
                        "example": {"Result": "Ingredient deleted",
                                    "id": 1,
                                    "name": "Cheese"},
                    }
                },
            }
        },
    },
}