import axios from "axios";

export const api = axios.create({
    baseURL: "https://postly-api-axyk.onrender.com/api/v1",
    headers: {
        "Content-Type": "application/json"
    },
    withCredentials: true,
    
})


api.interceptors.response.use(
    (resp)=> resp,
    async (error) => {
        // console.log(error?.response);

        
    if (error.config.url.includes("/auth/refresh") && (error?.response?.status === 401 || error?.response?.status === 403)) {
            // window.location  = "/auth/login"
            console.log(error?.response);
            
            return Promise.reject(error)
        }

        if(error?.response?.status === 422){
            return { error: `ERR_${error?.response?.statusText}_${error?.response?.status}: Validation Error`}          
        }

        if (error?.response?.status !== 401) {
            return {error: `ERR_${error?.response?.statusText}_${error?.response?.status}: ${error?.response?.data?.detail}`}
        }
  
        if (error?.response?.status === 401 && !error.config._retry) {

            console.log(error?.response);
            

            error.config._retry = true
            // // make request to /auth/refresh

            try {
                const response = await api.get("/auth/refresh")
                console.log(response);
                
                // return api(error?.config)

            } catch (error) {
                // window.location = "/auth/login"
                console.log(error?.response);

                return Promise.reject(error)
            }
        }
    }

)

