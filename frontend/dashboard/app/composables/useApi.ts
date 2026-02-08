import type { Quiz, QuizResult, QuizSource, CreateQuizPayload } from '~/types'

export const useApi = () => {
  const { $fetch } = useNuxtApp()
  const config = useRuntimeConfig()

  const getAuthHeaders = () => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
    return {
      Authorization: `Bearer ${token}`
    }
  }

  // Quiz Endpoints
  const getMyQuizzes = async () => {
    return $fetch<Quiz[]>('/api/quizzes/my_quizzes', {
      method: 'GET',
      headers: getAuthHeaders()
    })
  }

  const getQuiz = async (quizId: number) => {
    return $fetch<Quiz>(`/api/quizzes/${quizId}`, {
      method: 'GET',
      headers: getAuthHeaders()
    })
  }

  const deleteQuiz = async (quizId: number) => {
    return $fetch(`/api/quizzes/${quizId}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    })
  }

  const submitQuiz = async (quizId: number, userAnswers: any) => {
    return $fetch<QuizResult>(`/api/quizzes/submit/${quizId}`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: {
        user_answers: userAnswers
      }
    })
  }

  // Quiz Creation
  const createQuiz = async (payload: CreateQuizPayload) => {
    const formData = new FormData()
    formData.append('quiz_name', payload.quiz_name)
    formData.append('quiz_type', payload.quiz_type)
    formData.append('num_questions', payload.num_questions.toString())
    formData.append('time_limit', payload.time_limit.toString())

    if (payload.file) {
      formData.append('file', payload.file)
    } else if (payload.source_id) {
      formData.append('source_id', payload.source_id.toString())
    }

    return $fetch<Quiz>('/api/quizzes/create', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: formData
    })
  }

  // Quiz Sources (PDF uploads)
  const getSources = async () => {
    return $fetch<QuizSource[]>('/api/sources', {
      method: 'GET',
      headers: getAuthHeaders()
    })
  }

  const uploadSource = async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)

    return $fetch<QuizSource>('/api/sources/upload', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: formData
    })
  }

  const deleteSource = async (sourceId: number) => {
    return $fetch(`/api/sources/${sourceId}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    })
  }

  // Quiz Results
  const getQuizResult = async (resultId: number) => {
    return $fetch<QuizResult>(`/api/results/${resultId}`, {
      method: 'GET',
      headers: getAuthHeaders()
    })
  }

  return {
    getMyQuizzes,
    getQuiz,
    deleteQuiz,
    submitQuiz,
    createQuiz,
    getSources,
    uploadSource,
    deleteSource,
    getQuizResult
  }
}
