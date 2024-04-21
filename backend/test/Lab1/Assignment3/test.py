import json, os


fabricated_validator_file_name = 'fabricated_collection'
json_string = {"$jsonSchema": {
                            "bsonType": "object",
                            "required": ["just"],
                            "properties": {
                                "bsonType": "string",
                                "just": "mocking",
                                "uniqueItems": True
                            }
                        }
                    }
# Create the validator file
with open(fabricated_validator_file_name, 'w') as outfile:
    json.dump(json_string, outfile)

os.remove(fabricated_validator_file_name)
