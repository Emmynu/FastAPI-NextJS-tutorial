"use client"
import { useAuth } from "../api/auth"
import Link from "next/link"
import { useQuery } from "@tanstack/react-query"


export default  function Profile() {
    const { getCurrentUser } = useAuth()

    const { data:user, isLoading } =  useQuery({
        queryKey: ["currentUser"],
        queryFn: async()=>{
           return await getCurrentUser()
        },
        staleTime: 36000* 60* 15
    })
  
    
    if (user?.error) {
        return(
            <h2 className="text-error">{user?.error}</h2>
        )
    }
    

    return (
        <>
            <h1>PROFILE</h1>
            <main>
                {isLoading ?<h2>Loading...</h2>: <div>
                    <h2>{user?.data?.user?.username}</h2>
                    <h4>{user?.data?.user?.email}</h4>
                    </div>}
                <button className="btn btn-warning font-extrabold mr-1"><Link href={"/posts"}>Back</Link></button>
            </main>
        </>
    )
}