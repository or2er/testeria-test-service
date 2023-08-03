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
{
    "questions": [
        {
            "number": 1,
            "content": [
                "Nếu ",
                {
                    "inline_image": "image1.wmf"
                },
                " thì ",
                {
                    "inline_image": "image2.wmf"
                },
                " bằng"
            ],
            "choices": [
                [
                    {
                        "inline_image": "image3.wmf"
                    },
                    "."
                ],
                [
                    {
                        "inline_image": "image4.wmf"
                    },
                    "."
                ],
                [
                    {
                        "inline_image": "image5.wmf"
                    },
                    "."
                ],
                [
                    {
                        "inline_image": "image6.wmf"
                    },
                    "."
                ]
            ]
        },
        {
            "number": 2,
            "content": [
                "Cho khối lăng trụ có diện tích đáy là ",
                {
                    "inline_image": "image7.wmf"
                },
                "và chiều cao ",
                {
                    "inline_image": "image8.wmf"
                },
                " Thể tích khối lăng trụ đã cho bằng"
            ],
            "choices": [
                [
                    {
                        "inline_image": "image9.wmf"
                    },
                    "."
                ],
                [
                    {
                        "inline_image": "image10.wmf"
                    },
                    "."
                ],
                [
                    {
                        "inline_image": "image11.wmf"
                    },
                    "."
                ],
                [
                    {
                        "inline_image": "image12.wmf"
                    },
                    "."
                ]
            ]
        },
        ...
        {
            "number": 50,
            "content": [
                "Có bao nhiêu giá trị nguyên dương của tham số ",
                {
                    "inline_image": "image361.wmf"
                },
                " để hàm số ",
                {
                    "inline_image": "image362.wmf"
                },
                " có đúng ba điểm cực trị "
            ],
            "choices": [
                [
                    {
                        "inline_image": "image363.wmf"
                    },
                    "."
                ],
                [
                    {
                        "inline_image": "image364.wmf"
                    },
                    "."
                ],
                [
                    {
                        "inline_image": "image365.wmf"
                    },
                    "."
                ],
                [
                    {
                        "inline_image": "image366.wmf"
                    },
                    ". "
                ]
            ]
        }
    ]
}
```

- `GET /data/:id/answers`

### Output
```json
{
    "answers": [
        {
            "number": 1,
            "answer": 0
        },
        {
            "number": 2,
            "answer": 1
        },
        {
            "number": 3,
            "answer": 3
        },
        {
            "number": 4,
            "answer": 2
        },
        ...
        {
            "number": 50,
            "answer": 0
        }
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
