import groq

# Replace with your actual Groq API key
GROQ_API_KEY = "GROK API key here."
client = groq.Groq(api_key=GROQ_API_KEY)

try:
    response = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[{"role": "user", "content": "Enhance my resume."}],
        temperature=0.7,
        max_tokens=800
    )
    
    print("API Response:", response.choices[0].message.content)

except Exception as e:
    print("API Error:", str(e))
