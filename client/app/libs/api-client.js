import axios from "axios";

export const api = axios.create({
    baseURL: "/api/v1",
    headers: {
        "Content-Type": "application/json"
    },
    withCredentials: true,
    
})


api.interceptors.response.use(
    (resp)=> resp,
    async (error) => {


        if(error?.response?.status === 422){
            return { error: `ERR_${error?.response?.statusText}_${error?.response?.status}: Validation Error`}          
        }

        if (error?.response?.status !== 401) {
            return {error: `ERR_${error?.response?.statusText}_${error?.response?.status}: ${error?.response?.data?.detail}`}
        }
  
        if (error?.response?.status === 401 ) {
            if(error.config.url.includes("/auth/login")){
                return {error: `ERR_${error?.response?.statusText}_${error?.response?.status}: ${error?.response?.data?.detail}`}
            }

            if(!error.config._retry){
                error.config._retry = true
                // make request to /auth/refresh

                try {
                    const resp = await api.get("/auth/refresh")   

                    if (resp?.error) {
                       window.location = "/auth/login"
                    }
                    
                    return api(error?.config)

                } catch (error) {
                    window.location = "/auth/login"  
                    return Promise.reject(error)
                }
            }
        }
    }

)

