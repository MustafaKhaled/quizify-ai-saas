// User Authentication
export interface User {
  id: number
  email: string
  name: string
  is_admin: boolean
  is_pro: boolean
  trial_ends_at: string | null
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user?: User
}

export interface SubscriptionInfo {
  is_pro: boolean
  trial_ends_at: string | null
  trial_days_remaining: number
}

// Quiz Types
export type QuizType = 'single_choice' | 'multiple_select' | 'matching'

export interface Question {
  id: string
  question_text: string
  options: string[]
  correct_answer: string | string[]
  explanation?: string
}

export interface Quiz {
  id: number
  user_id: number
  source_id?: number
  title: string
  quiz_type: QuizType
  num_questions: number
  time_limit: number
  content: Question[]
  generation_date: string
}

export interface QuizSource {
  id: number
  user_id: number
  file_name: string
  extracted_text: string
  upload_date: string
  start_page?: number
  end_page?: number
}

export interface CreateQuizPayload {
  quiz_name: string
  quiz_type: QuizType
  num_questions: number
  time_limit: number
  file?: File
  source_id?: number
}

// Quiz Taking
export interface UserAnswer {
  question_id: string
  answer: string | string[]
}

export interface QuizSubmitPayload {
  user_answers: UserAnswer[]
}

// Results
export interface QuizResult {
  id: number
  quiz_id: number
  user_id: number
  score_percentage: number
  is_passed: boolean
  time_taken_seconds: number
  user_answers: UserAnswer[]
  attempt_date: string
}

// API Response Types
export interface ApiResponse<T> {
  data: T
  status: number
  message?: string
}

export interface ApiError {
  detail: string
  status?: number
}

// Dashboard Stats
export interface DashboardStats {
  total_quizzes: number
  average_score: number
  quizzes_taken: number
  recent_quizzes: Quiz[]
}
