recipe_examples = {
    "get_all": {
        "responses": {
            200: {
                "description": "Recipe list",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "id": 1,
                                "author_id": 101,
                                "cooking_time_in_minutes": 30,
                                "image_url": "https://example.com/image1.jpg",
                                "ingredients": [
                                    {"ingredient_id": 1, "quantity": 100, "unit_id": 1},
                                    {"ingredient_id": 2, "quantity": 200, "unit_id": 2}
                                ]
                            },
                            {
                                "id": 2,
                                "author_id": 102,
                                "cooking_time_in_minutes": 15,
                                "image_url": "https://example.com/image2.jpg",
                                "ingredients": [
                                    {"ingredient_id": 3, "quantity": 50, "unit_id": 1}
                                ]
                            }
                        ]
                    }
                }
            }
        }
    },

    "get_one": {
        "responses": {
            200: {
                "description": "Recipe details",
                "content": {
                    "application/json": {
                        "example": {
                            "id": 1,
                            "author_id": 101,
                            "cooking_time_in_minutes": 30,
                            "image_url": "https://example.com/image1.jpg",
                            "ingredients": [
                                {"ingredient_id": 1, "quantity": 100, "unit_id": 1},
                                {"ingredient_id": 2, "quantity": 200, "unit_id": 2}
                            ]
                        }
                    }
                }
            }
        }
    },

    "create": {
        "requestBody": {
            "description": "Data to create a new recipe",
            "content": {
                "application/json": {
                    "example": {
                        "author_id": 101,
                        "cooking_time_in_minutes": 30,
                        "image_url": "https://example.com/image1.jpg",
                        "ingredients": [
                            {"ingredient_id": 1, "quantity": 100, "unit_id": 1},
                            {"ingredient_id": 2, "quantity": 200, "unit_id": 2}
                        ]
                    }
                }
            }
        }
    },

    "update": {
        "requestBody": {
            "description": "Data to update an existing recipe",
            "content": {
                "application/json": {
                    "example": {
                        "cooking_time_in_minutes": 25,
                        "image_url": "https://example.com/new_image.jpg",
                        "ingredients": [
                            {"ingredient_id": 1, "quantity": 150, "unit_id": 1},
                            {"ingredient_id": 3, "quantity": 50, "unit_id": 2}
                        ]
                    }
                }
            }
        }
    },

    "delete": {
        "responses": {
            200: {
                "description": "Deleted recipe response",
                "content": {
                    "application/json": {
                        "example": {
                            "Result": True,
                            "id": 1,
                            "name": "Spaghetti Carbonara"
                        }
                    }
                }
            }
        }
    }
}
