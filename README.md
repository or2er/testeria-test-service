# IAI Hackathon 2023 - Testeria - Flask Test Service

## Usage

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run server
```bash
python server.py
```

## API

- `POST /api/quiz2quiz`

### Input (form-data)
```json
{
  "file": <file>
}
```

- `GET /data/:id/questions`

### Output (json file)
```json
"questions": [
    {
      "content": ["What is the capital of France?"],
      "choices": [["Paris"], ["London"], ["Berlin"], ["Madrid"]],
    },
    {
      "content": [
        "What is the capital of ",
        { "text": "France", "style": ["bold", "italic"] },
        "?"
      ],
      "choices": [["Paris"], ["London"], ["Berlin"], ["Madrid"]],
    },
    {
      "content": ["Where is this place?", { "image": "image-0.jpg" }],
      "choices": [["Paris"], ["London"], ["Berlin"], ["Madrid"]],
    },
    {
      "content": [
        "Given",
        { "inline-image": "image-1.jpg" },
        "and",
        { "inline-image": "image-2.jpg" },
        "what is the value of",
        { "inline-image": "image-3.jpg" }
      ],
      "choices": [
        [{ "inline-image": "image-4.jpg" }],
        [{ "inline-image": "image-5.jpg" }],
        [{ "inline-image": "image-6.jpg" }],
        [{ "inline-image": "image-7.jpg" }]
      ],
    }
  ]
```

- `GET /data/:id/answers`

### Output
```json
{
  "answers": [
    1, 
    0,
    3,
    2,
    3,
  ]
}
```

### Output
```json
{
  "testid": "00edc848672c4ec99e80947a0d8ee9ed",
  "num_questions": 10,
}
```

- `GET /data/:id/media/:id/:filename`

Get image of the document using document id and filename.

Example: `GET /data/00edc848672c4ec99e80947a0d8ee9ed/media/image1.png`