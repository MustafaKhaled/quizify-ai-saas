// admin/auth.d.ts
declare module '#auth-utils' {
    interface User {
      id: number
      email: string
      name: string
      is_admin: boolean
    }
  
    interface UserSession {
      user: User
      token: string
    }
  }
  
  export {}
  