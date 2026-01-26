# Quizify Dashboard

User-facing dashboard for creating and taking quizzes from PDF documents.

## Setup

1. Install dependencies:
```bash
pnpm install
```

2. Create a `.env` file with:
```
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
NUXT_SESSION_PASSWORD=your-secret-session-password-here
```

3. Run the development server:
```bash
pnpm dev
```

## Features

- **PDF Upload**: Upload PDF files to extract text and generate quiz questions
- **Quiz Generation**: Create quizzes with single choice or multiple select questions
- **Quiz Taking**: Take quizzes with timer support and real-time feedback
- **Results Review**: View detailed results with explanations for each question
- **Account Management**: Update profile and view subscription status

## Pages

- `/` - Dashboard overview
- `/login` - User login
- `/signup` - User registration
- `/upload` - Upload PDF and create quiz
- `/quizzes` - List all user's quizzes
- `/quiz/[id]` - Take a quiz
- `/account` - Account settings
