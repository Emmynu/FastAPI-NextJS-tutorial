import { api } from "@/app/libs/api-client"
import { useState } from "react"


export  function useAuth() {
    const delay = (ms) => new Promise(resolve=> setTimeout(resolve, ms))
    const [isLoading, setIsLoading] = useState(false)

    
    return{
      async login(data, ms= 2000){

          setIsLoading(true)
          await delay(ms)
          const response = await api.post("/auth/login", data).finally(setIsLoading(false))
          return response
       
      },
      
      async signUp(data, ms= 2000){

            setIsLoading(true)

            await delay(ms)
            const response = await api.post("/auth/signup", data).finally(setIsLoading(false))
            return response

      },

      async getCurrentUser() {

        const response = await api.get("/auth/profile")
        return response
        
      },

      async signOut() {
        setIsLoading(true)

         await delay(2000)
         await api.get("/auth/logout").finally(setIsLoading(false))
         window.location.reload()

      },
    isLoading
}
}