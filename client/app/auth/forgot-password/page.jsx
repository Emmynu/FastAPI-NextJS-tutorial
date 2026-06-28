"use client"

import { showToast } from "@/app/libs/toast"
import { useAuth } from "../api/auth"
import Link from "next/link"
import "../auth.css"

export default function ForgotPassword() {
    const { forgotPassword } =  useAuth()

    async function handleSubmit(e) {
        e.preventDefault()

        const data =  Object.fromEntries(new FormData(e.currentTarget))

        if (data.email.length > 0) {
           const  resp = await forgotPassword(data)
           console.log(resp)
            if (resp?.status === 200){
                showToast({ type: "success", title: resp?.data?.msg, msg: null})
        }
        else{
            showToast({type: "error", title: "Oops!...something went wrong", msg:resp?.error})
        }
        }else{
            showToast({type:"error", title: "Invalid input", msg: "Provide a valid email"})
        }
        

    }
    return(
           <main className="m-9">
            <h1 className="text-xl  font-medium">Reset Password</h1>
            <form  onSubmit={handleSubmit} className="mt-2">
                 <label className="input  validator">
                        <svg className="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <g
                        strokeLinejoin="round"
                        strokeLinecap="round"
                        strokeWidth="2.5"
                        fill="none"
                        stroke="currentColor"
                        >
                        <rect width="20" height="16" x="2" y="4" rx="2"></rect>
                        <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
                        </g>
                        </svg>
                        <input type="email" placeholder="mail@site.com" required name="email"/>
                    </label>
                    <div className="validator-hint hidden">Enter valid email address</div>
                
                <section className="mt-2 mb-3">
                    <h2 className="text-sm ">Remember password? <Link href={"/auth/login"} className="italic hover:underline ">Login</Link></h2>
                </section>

                <button type="submit" className="btn btn-warning ">Submit</button>
        </form>
        </main>
    )
}