"use client"
import { useAuth } from "../api/auth"
import { showToast } from "@/app/libs/toast"
import "../../globals.css"
import "../auth.css"
import { useRouter } from "next/navigation"
import Link from "next/link"


export default function Register() {
    const { signUp, isLoading } =  useAuth()
    const router =  useRouter()

    async function handleRegister(e){
       
        e.preventDefault()
        const { userName, password, email } = Object.fromEntries(new FormData(e.currentTarget))
        

        const data = {
            username: userName,
            firstName: userName,
            lastName: userName,
            password,
            email
        }

        const resp =  await signUp(data)
        
        if (resp?.status === 201) {
            showToast({ type: "success", title: "Registration Successful", msg:null })
            router.push("/auth/login")
        }else{   
            showToast({ type: "error", title: "Failed to register", msg:resp?.error })
    }
    

    
    }

    return(
        <main className="m-9" >
            <h1 className="text-xl  font-medium">Create Your Account</h1>
            <form onSubmit={handleRegister} >
                <section className="my-3">
                    <label className="input validator">
                        <svg className="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                            <g
                            strokeLinejoin="round"
                            strokeLinecap="round"
                            strokeWidth="2.5"
                            fill="none"
                            stroke="currentColor"
                            >
                            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
                            <circle cx="12" cy="7" r="4"></circle>
                            </g>
                        </svg>
                        <input
                            type="text"
                            required
                            name="userName"
                            placeholder="Username"
                            pattern="[A-Za-z][A-Za-z0-9\-]*"
                            minLength="3"
                            maxLength="30"
                            title="Only letters, numbers or dash"
                        />
                </label>
                <p className="validator-hint hidden">Must be 3 to 30 characters</p>
                </section>

                <section className="my-3">
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
                </section>



                <section className="my-3">
                    <label className="input validator">
                        <svg className="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                            <g
                            strokeLinejoin="round"
                            strokeLinecap="round"
                            strokeWidth="2.5"
                            fill="none"
                            stroke="currentColor"
                            >
                            <path
                                d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"
                            ></path>
                            <circle cx="16.5" cy="7.5" r=".5" fill="currentColor"></circle>
                            </g>
                        </svg>
                        <input
                            type="password"
                            required
                            name="password"
                            placeholder="Password"
                            minLength="7"
                            maxLength="12"
                            pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                            title="Must be more than 8 characters, including number, lowercase letter, uppercase letter"
                        />
                </label>
                <p className="validator-hint hidden">
                Must be more than 8 characters, including
                <br />At least one number <br />At least one lowercase letter <br />At least one uppercase letter
                </p>
                </section>

                <section>
                    <h2 className="text-sm mb-3">Already have an account? <Link href={"/auth/login"} className="italic hover:underline ">Login</Link></h2>
                </section>

                <button className="btn btn-warning " disabled={isLoading}>{isLoading ? <h2><span className="loading loading-spinner loading-sm mx-1"></span>Loading...</h2>: "Continue"}</button>
                
            </form>
        </main>
    )
}