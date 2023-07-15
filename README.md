## Convert .docx to .json

### Output

```json
{
  "questions": [
    {
      "content": "What is the capital of France?",
      "choices": ["Paris", "London", "Berlin", "Madrid"],
      "answer": 0
    },
    {
      "content": [
        "What is the capital of ",
        { "text": "France", "style": ["bold", "italic"] },
        "?"
      ],
      "choices": ["Paris", "London", "Berlin", "Madrid"],
      "answer": 0
    },
    {
      "content": ["Where is this place?", { "image": "https://example.com" }],
      "choices": ["Paris", "London", "Berlin", "Madrid"],
      "answer": 0
    },
    {
      "content": [
        "Given",
        { "inline-image": "https://example.com/equation-1" },
        "and",
        { "inline-image": "https://example.com/equation-2" },
        "what is the value of",
        { "inline-image": "https://example.com/equation-3" }
      ],
      "choices": [
        { "inline-image": "https://example.com/equation-4" },
        { "inline-image": "https://example.com/equation-5" },
        { "inline-image": "https://example.com/equation-6" },
        { "inline-image": "https://example.com/equation-7" }
      ],
      "answer": 0
    }
  ]
}
```
