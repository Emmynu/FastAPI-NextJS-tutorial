"use client"
import Link from "next/link";



 export default function Page() {

  return(
    <div className="ml-10 mt-5">
      <h1 className="text-2xl font-bold">FastAPI and NextJS Tutorial</h1>

      <section className="mt-3 flex ">
        <Link href={"/auth/register"} className="btn ml-2 btn-warning">Sign up</Link>
        <Link href={"/auth/login"} className="btn ml-2 btn-warning">Login</Link>
        <Link href={"https://postly-api-axyk.onrender.com/docs"} className="btn ml-2 btn-warning">Documentation</Link>
      </section>
    </div>
  )
}