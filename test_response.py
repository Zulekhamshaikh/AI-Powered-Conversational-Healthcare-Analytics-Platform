from utils.load_data import load_data
from ai.response_generator import generate_response

df = load_data()

print(generate_response(df))